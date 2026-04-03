import json
import os
import sys
import time
import uuid

import streamlit as st
from chat import ChatManager, invoke_endpoint_streaming
from chat_utils import make_urls_clickable
from streamlit_cognito_auth import CognitoAuthenticator

# Get the current file's directory and add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from utils import get_customer_support_secret

# -------------------------------------------------------------------
# Auth and runtime configuration
# -------------------------------------------------------------------
secret = get_customer_support_secret()
secret = json.loads(secret)

authenticator = CognitoAuthenticator(
    pool_id=secret["pool_id"],
    app_client_id=secret["client_id"],
    app_client_secret=secret["client_secret"],
    use_cookies=False,
)

is_logged_in = authenticator.login()
if not is_logged_in:
    st.stop()


def logout():
    authenticator.logout()


CONTEXT_WINDOW = 10
qualifier = "DEFAULT"


def build_context(messages, context_window=CONTEXT_WINDOW):
    history = (
        messages[-context_window * 2 :]
        if len(messages) > context_window * 2
        else messages
    )
    context = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n"
    return context


def format_response_text(text: str) -> str:
    if not text:
        return text

    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

    text = text.replace('\\"', '"')
    text = text.replace('\\n', '\n')
    text = text.replace('\\t', '\t')
    text = text.replace('\\r', '\r')
    return text


def extract_final_answer(accumulated_response: str) -> str:
    try:
        begin_marker = '"Begin agent execution"'
        end_marker = '"End agent execution"'

        begin_pos = accumulated_response.find(begin_marker)
        end_pos = accumulated_response.find(end_marker)

        if begin_pos != -1 and end_pos != -1:
            json_part = accumulated_response[
                begin_pos + len(begin_marker) : end_pos
            ].strip()

            json_start = json_part.find('{"role":')
            if json_start != -1:
                json_str = json_part[json_start:]

                brace_count = 0
                json_end = -1
                for i, char in enumerate(json_str):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break

                if json_end != -1:
                    json_str = json_str[:json_end]
                    response_data = json.loads(json_str)

                    if (
                        "content" in response_data
                        and len(response_data["content"]) > 0
                        and "text" in response_data["content"][0]
                    ):
                        return response_data["content"][0]["text"]
    except Exception:
        pass

    return accumulated_response


st.set_page_config(
    page_title="Secure AI CTI Assistant",
    page_icon="🛡️",
    layout="wide",
)

with st.sidebar:
    st.text(f"Welcome,\n{authenticator.get_username()}")
    st.button("Logout", "logout_btn", on_click=logout)

    st.markdown("---")
    st.markdown("### Suggested demo questions")
    st.markdown(
        """
- Is this IP address 14.143.247.202 malicious?
- Is this IP address 14.143.210.2 malicious?
- Is this hash d01e27462252c573f66a14bb03c09dd2 malicious?
- What vulnerability does Salt Typhoon exploit?
- Is this domain malicious-c2.com malicious?
- Find threat actor using IP 167.88.173.252
- Tell me more about T1078
- Who uses CVE-2024-21762?
- Is the IP address 8.8.8.8 malicious?
- Is this domain malicious: nikeoutletinc.org?
- Is this hash malicious: 5db340a70cb5d90601516db89e629e43?
        """
    )

st.title("🛡️ Secure AI CTI Assistant")
st.caption(
    "Dataset grounded CTI assistant for malware analysis, IOC lookup, threat actor attribution, and safe refusal when information is not present in the dataset."
)

chat_manager = ChatManager("default")

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_assistant" not in st.session_state:
    st.session_state["pending_assistant"] = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask a CTI question in English..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        start_time = time.time()
        accumulated_response = ""
        answer = ""

        try:
            session_id = st.session_state.get("session_id")
            context = build_context(st.session_state.messages, CONTEXT_WINDOW)
            payload = json.dumps({"prompt": context})
            bearer_token = st.session_state.get("auth_access_token")

            message_placeholder.markdown(
                '<span class="thinking-bubble">🛡️ 🔎 CTI Assistant is analyzing...</span>',
                unsafe_allow_html=True,
            )

            for chunk in invoke_endpoint_streaming(
                agent_arn=st.session_state["agent_arn"],
                payload=payload,
                session_id=session_id,
                bearer_token=bearer_token,
                endpoint_name=qualifier,
            ):
                if not chunk.strip():
                    continue

                accumulated_response += chunk

                if '\"End agent execution\"' in accumulated_response or '"End agent execution"' in accumulated_response:
                    message_placeholder.markdown(
                        '<span class="thinking-bubble">🛡️ 📊 Finalizing response...</span>',
                        unsafe_allow_html=True,
                    )
                    break

                streaming_text = make_urls_clickable(accumulated_response)
                message_placeholder.markdown(
                    f'<div class="assistant-bubble streaming">🛡️ {streaming_text}</div>',
                    unsafe_allow_html=True,
                )
                time.sleep(0.02)

            answer = extract_final_answer(accumulated_response)
            answer = format_response_text(answer)
            clickable_answer = make_urls_clickable(answer)

            elapsed = time.time() - start_time
            message_placeholder.markdown(
                f'<div class="assistant-bubble">🛡️ {clickable_answer}<br><span style="font-size:0.9em;color:#888;">⏱️ Response time: {elapsed:.2f} seconds</span></div>',
                unsafe_allow_html=True,
            )

        except Exception as e:
            elapsed = time.time() - start_time
            answer = f"Sorry, I encountered an error: {str(e)}"
            message_placeholder.markdown(
                f'<div class="assistant-bubble">🛡️ ❌ {answer}</div>',
                unsafe_allow_html=True,
            )

        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "elapsed": elapsed}
        )

        st.session_state["pending_assistant"] = False
        st.rerun()
