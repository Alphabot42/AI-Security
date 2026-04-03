<p align="center">
⭐ <b>If you find this demo useful, consider starring the repository!</b>
</p>

# 🛡️ Secure AI CTI Assistant – Chatbot Demo (09B3)

---

## 🎯 Demo Overview

This project demonstrates a **secure, dataset-grounded AI chatbot for Cyber Threat Intelligence (CTI)**.

Unlike traditional AI assistants, this chatbot:

- ❌ Does NOT hallucinate
- ❌ Does NOT invent data
- ✅ Only answers from trusted CTI data
- ✅ Refuses safely when information is missing

👉 This is a **realistic CTI assistant demo for SOC analysts and security teams**.

---

## 🧠 What This Demo Shows

This chatbot can:

- Check if an **IP address is malicious**
- Analyze **hashes and domains**
- Perform **threat actor attribution**
- Map activity to **MITRE ATT&CK techniques**
- Answer CTI questions **in real time**

---

## 💬 Example Questions

```
Is this IP address 14.143.247.202 malicious?
Is this hash d01e27462252c573f66a14bb03c09dd2 malicious?
Find threat actor using IP 167.88.173.252
Tell me more about T1078
What vulnerability does Salt Typhoon exploit?
```

---

## 🧪 Example Output

```
IP: 14.143.247.202 → malicious

Actor: Salt Typhoon
Type: State-sponsored espionage

Capabilities:
- Credential abuse
- Network device compromise
- Data exfiltration

MITRE ATT&CK:
- T1078 (Valid Accounts)
- T1090 (Proxy / Tunneling)
- T1041 (Exfiltration over C2)
```

---

## ⚙️ Architecture (Simplified)

```
User (Chat UI)
      ↓
Streamlit Chatbot (Frontend)
      ↓
CTI Runtime (AWS AgentCore)
      ↓
Secure CTI Backend
      ↓
Dataset (trusted source only)
```

---

## 🔐 Security Features

This chatbot is designed with **AI security in mind**:

- Prompt injection resistance
- Dataset grounding (no external hallucination)
- Safe refusal when data is missing
- Controlled response generation
- No leakage of sensitive data

---

## 🚀 How to Run

From your AWS SageMaker environment:

```bash
cd lab_helpers/lab5_frontend/
streamlit run main.py
```

Then open the provided URL.

Login:
```
Username: testuser
Password: MyPassword123!
```

---

## 🖥️ Demo UI

👉 Chat interface with:
- Suggested CTI queries
- Real-time responses
- Secure interaction with backend

---

## ⚠️ Important Design Choice

This demo is intentionally:

👉 **Dataset-grounded only**

Meaning:
- If data is not present → the assistant refuses
- No guessing
- No hallucination

---

## 🔮 What Comes Next (09C)

Next step: **Multi-source CTI assistant**

Future version will integrate:

- VirusTotal
- AbuseIPDB
- OSINT sources
- OpenCTI / MISP
- MITRE ATT&CK live enrichment

---

## 👩‍💻 Author

AI Security Specialist focused on:

- Malware analysis
- Cyber Threat Intelligence
- LLM security
- Adversarial AI

---

## ⭐ Support

If you like this demo:

👉 Star the repo  
👉 Share it  
👉 Use it in your research  

---
