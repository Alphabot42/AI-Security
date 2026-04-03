<p align="center">
⭐ <b>If you find this work useful, consider starring the repository!</b>
</p>

# 🛡️ Experiment 09 – AI Assisted Cyber Threat Intelligence

---

## 🎯 Overview

This experiment explores how Large Language Models (LLMs) can assist Cyber Threat Intelligence (CTI) analysts while ensuring:

- Reliability (no hallucination)
- Security (safe prompt handling)
- Trustworthiness (grounded answers)
- Controlled behavior (safe refusal when needed)

Unlike generic AI assistants, this project focuses on **defensive AI security applied to CTI workflows**.

---

## 🧠 Key Concept

The goal is to build a **Secure CTI Assistant** that:

- Answers CTI questions (IP, hash, domain, threat actor, MITRE TTPs)
- Uses **trusted data sources only**
- Avoids hallucinations
- Clearly refuses when information is missing
- Evolves toward a **multi-source CTI enrichment engine**

---

## 🏗️ Project Structure

```
Experiment 09/
│
├── 09a_Secure_AI_CTI_Assistant
│   → Local prototype (dataset-grounded)
│
├── 09b_SecureAI_CTI_Assistant_on_AWS
│   → Production-ready agent (Bedrock + AgentCore)
│
├── 09c_Multi-source_enriched_CTI_assistant
│   → Next step: real-world CTI assistant (OSINT + APIs)
│
└── README.md
```

---

## ⚙️ Architecture

### 🔹 09A – Local Secure CTI Assistant

- Dataset-driven
- No external calls
- Safe and deterministic behavior

👉 Goal: **prove reliability and security**

---

### 🔹 09B – Production CTI Assistant (AWS)

Built using:

- Amazon Bedrock
- AgentCore Runtime
- Secure memory and identity
- Streamlit frontend chatbot

👉 Features:

- Real-time chatbot interface
- Authentication (Cognito)
- Secure runtime invocation
- Dataset-grounded responses only

👉 Goal: **POC → production-ready AI system**

---

### 🔹 09B3 – Interactive Chatbot Demo

Frontend (Streamlit):

- Chat interface
- Suggested CTI queries
- Live interaction with deployed agent
- Safe responses

Example queries:

```
Is this IP address malicious?
Is this hash malicious?
Find threat actor using IP
Tell me more about T1078
What vulnerability does Salt Typhoon exploit?
```

👉 Goal: **Demo for recruiters / real usage**

---

### 🔹 09C – Multi-Source CTI Assistant (Next Step)

🚨 This is where it becomes **real CTI**

Instead of relying only on a dataset:

The assistant will dynamically query:

- VirusTotal
- AbuseIPDB
- URLScan
- OpenCTI / MISP
- OSINT sources
- MITRE ATT&CK
- SOC logs / internal data

---

## 🧩 Target Architecture (09C)

```
User
  ↓
AI CTI Assistant (Orchestrator)
  ↓
Decision Engine (query classification)
  ↓
Multi-source connectors:
    - Internal dataset
    - OSINT APIs
    - Threat Intel platforms
  ↓
Aggregation & Scoring
  ↓
Final Answer (with sources + confidence)
```

---

## 🔐 Security Design

This project focuses on **Defensive AI Security**:

- Prompt injection resistance
- No hallucination policy
- Dataset grounding enforcement
- Safe refusal mechanism
- Output validation

---

## 🧪 Example Output

```
IP: 14.143.247.202 → malicious

Associated actor: Salt Typhoon
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

## 🚀 Why This Project Matters

Most AI assistants:

❌ hallucinate  
❌ mix sources  
❌ cannot be trusted in security  

This project demonstrates:

✅ Trustworthy AI  
✅ Controlled behavior  
✅ Security-first design  
✅ Real CTI use case  

---

## 🧭 Roadmap

- [x] 09A – Local secure assistant
- [x] 09B – AWS production deployment
- [x] 09B3 – Interactive chatbot demo
- [ ] 09C – Multi-source CTI enrichment
- [ ] Advanced correlation engine
- [ ] Confidence scoring
- [ ] Source attribution system

---

## 👩‍💻 Author

AI Security Specialist with a strong background in Malware Reverse Engineering and Cyber Threat Intelligence.

Focus:
- Adversarial AI
- LLM security
- CTI automation
- Secure AI pipelines

---

## ⭐ Support

If you like this project:

👉 Star the repo  
👉 Share it  
👉 Use it for research  

---
