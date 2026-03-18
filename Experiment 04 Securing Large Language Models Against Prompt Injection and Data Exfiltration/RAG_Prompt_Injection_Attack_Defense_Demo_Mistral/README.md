# 🛡️ Experiment 04 — Securing Mistral Against Prompt Injection & RAG Hijacking

## Overview

This project demonstrates how a modern LLM (Mistral via Ollama) can be exploited through:

- Prompt Injection (LLM01)
- Sensitive Data Leakage (LLM06)
- RAG Hijacking via malicious documents

It also shows how a **layered defense pipeline** can reduce data leakage from **100% to 0%**.

---

## 🎯 Objectives

- Simulate a vulnerable banking assistant
- Demonstrate real-world prompt injection attacks
- Show how RAG context can be poisoned
- Implement a hardened pipeline with 4 defense layers
- Compare vulnerable vs secured system

---

## 🏗️ Architecture

### Vulnerable Pipeline

- Sensitive data directly injected into prompt
- No input filtering
- No access control
- No context sanitization
- No output filtering

➡️ Result: Full data leakage

---

### Hardened Pipeline (4 Layers)

1. **Layer 1 — Input Guard**
   - Detect prompt injection patterns

2. **Layer 2 — Access Control**
   - Block sensitive queries without authentication

3. **Layer 3 — Context Guard**
   - Sanitize retrieved documents (RAG)

4. **Layer 4 — Output Guard**
   - Filter sensitive information in responses

---

## ⚔️ Attack Scenarios

The notebook includes 7 realistic attack techniques:

- System Prompt Extraction
- Role Override (Admin mode)
- Authority Spoofing
- Hypothetical Framing
- Roleplay Jailbreak
- Claimed Authentication
- Ignore Instructions Attack

---

## 🧪 RAG Hijacking

A malicious document is injected into the retrieval pipeline:

- Overrides security rules
- Forces disclosure of sensitive data

➡️ Demonstrates that:
> Attacks can come from context, not just user input

---

## 📊 Results

| Metric | Vulnerable | Hardened |
|------|----------|----------|
| Leak rate | 1.0 | 0.0 |
| Block rate | 0.0 | 1.0 |

---

## 🔐 Key Learnings

- LLM vulnerabilities are often **architectural**, not just adversarial
- Prompt injection can bypass weak protections
- RAG systems introduce a **new attack surface**
- Layered defenses significantly reduce risk

---

## 📁 Project Structure

- `notebook.ipynb` → main experiment
- `attack_results.csv` → prompt injection results
- `rag_attack_results.csv` → RAG hijacking results
- `attack_report.md` → detailed attack logs
- `rag_attack_report.md` → RAG attack logs

---

## 🚀 How to Run

1. Install Ollama
2. Pull model:
   ```bash
   ollama pull mistral
   ```
3. Run notebook

---

## 🧠 OWASP Mapping

- **LLM01 — Prompt Injection**
  - Input Guard
  - Context Guard

- **LLM06 — Sensitive Information Disclosure**
  - Access Control
  - Output Guard

---

## 👩‍💻 Author

Natacha (Naty) — CTI & Malware Analysis  
Experimenting with AI Security, LLM attacks & defenses

---

## 💬 Final Note

This project is part of a broader AI Security research track.

Feel free to test, modify the attacks, and experiment with your own datasets.

👉 Enjoy and have a great secure day!
