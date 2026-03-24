
# AI Security Research Projects
### Adversarial Machine Learning | LLM Security | AI for Cybersecurity

This repository contains a collection of practical AI security research projects exploring adversarial machine learning, large language model security, and the application of AI techniques to cybersecurity domains such as cyber threat intelligence, malware analysis, and digital forensics.

The objective of these experiments is to understand how machine learning systems can be attacked, manipulated, and defended in real-world scenarios. Many experiments are mapped to the OWASP Top 10 Risks for LLM Applications to align with modern AI security practices.

This repository is structured as a progressive research roadmap, starting from adversarial ML fundamentals and advancing toward applied AI security use cases.

---

# Research Phases

The projects are organized into five progressive phases:

1. Adversarial ML Foundations
2. Modern Models (HF, LLM)
3. Training Pipeline Attacks
4. Defense Systems and Real world Use Cases
5. Applied AI for Cybersecurity (Malware, CTI and Forensics)

---

# Research Roadmap

```text
| Phase                              | Experiment                                      | Notebook                         | OWASP AI Top 10                         | Skills                               | Progress |
|-----------------------------------|-------------------------------------------------|----------------------------------|-----------------------------------------|--------------------------------------|----------|
| Phase 1 – Adversarial ML          | Practical Adversarial Attacks on Vision Models  | adversarial_samples_cifar10_demo | LLM02 Insecure Output Handling          | Offensive AI Security                | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02 LLM security series          | LLM02 Insecure Output Handling          | Offensive / Defensive AI Security    | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02b pretrained variant          | LLM02 Insecure Output Handling          | Offensive / Defensive AI Security    | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02c HF optimized                | LLM04 Model Denial of Service           | Offensive / Defensive AI Security    | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02d HF detector 16 threads      | LLM09 Overreliance                      | Offensive / Defensive AI Security    | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02e train detector MNIST        | LLM09 Overreliance                      | Offensive / Defensive AI Security    | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02f input transform defense     | LLM09 Overreliance                      | Offensive / Defensive AI Security    | ██████████ 100% |
| Phase 2 – Modern Models (LLM)     | Evasion Attack on Sentiment Analysis            | HFexplore_Llama evasion attack  | LLM01 Prompt Injection, LLM06 SID       | Offensive / Defensive AI Security    | █████░░░░░ 50% |
| Phase 2 – Modern Models (LLM)     | Securing LLMs Against Prompt Injection          | Mistral prompt injection defenses  | LLM01 Prompt Injection, LLM06 SID       | Defensive AI Security                | ██████████ 100% |
| Phase 2 – Modern Models (LLM)     | Securing LLMs Against Prompt Injection          | Attack_Defense_RAG_Hijacking  | LLM01 Prompt Injection, LLM06 SID       | Defensive AI Security                | ██████████ 100% |
| Phase 3 – Training Pipeline       | Membership Inference (Blackbox)                 | ART membership inference        | LLM06 Sensitive Information Disclosure  | Offensive AI Security                | ██░░░░░░░░ 25% |
| Phase 3 – Training Pipeline       | Model Stealing (Copycat)                        | model extraction attack         | LLM10 Model Theft                       | Offensive AI Security                | █░░░░░░░░░ 10% |
| Phase 3 – Training Pipeline       | Training Data Poisoning (Backdoor)              | ART poisoning attack            | LLM03 Training Data Poisoning           | Offensive AI Security                | █░░░░░░░░░ 10% |
| Phase 4 – Defense Systems         | Anomaly Detection on OT Pipeline                | OT anomaly detection            | LLM08 Excessive Agency                  | DPM / DS / ML / MLOps                | ██░░░░░░░░ 25% |
| Phase 5 – AI for Cybersecurity    | AI Assisted Cyber Threat Intelligence           | malware adversary tracking      | LLM06 SID, LLM07 Plugin Design          | Defensive AI Security                | ░░░░░░░░░░ 0% |
| Phase 5 – AI for Cybersecurity    | AI Assisted Malware Reverse Engineering         | AI malware deobfuscation        | LLM06 SID, LLM07 Plugin Design          | Defensive AI Security                | ░░░░░░░░░░ 0% |
| Phase 5 – AI for Cybersecurity    | AI Assisted Forensics                           | AI forensic investigation       | LLM06, LLM02, LLM08, LLM07              | Defensive AI Security                | ░░░░░░░░░░ 0% |
| Capstone                          | Detecting AI Powered Malware                    | AI malware detection system     | LLM08 Excessive Agency, LLM02 IOH       | Defensive AI Security                | ░░░░░░░░░░ 0% |
```

---

# OWASP AI Top 10 Coverage

| OWASP Risk | Covered Experiments |
|-------------|--------------------|
| LLM01 Prompt Injection | LLM Evasion Attacks, Prompt Injection Defense |
| LLM02 Insecure Output Handling | Adversarial ML Attacks |
| LLM03 Training Data Poisoning | Backdoor Poisoning |
| LLM04 Model Denial of Service | Adversarial Input Attacks |
| LLM06 Sensitive Information Disclosure | Membership Inference |
| LLM07 Insecure Plugin Design | AI Cybersecurity Tooling |
| LLM08 Excessive Agency | Autonomous Detection Systems |
| LLM09 Overreliance | Adversarial Detection |
| LLM10 Model Theft | Model Stealing Attacks |

---

# Repository Structure

```
AI Security
│
├── Experiment 01 Adversarial Examples in Practice Breaking a Vision Model with FGSM
├── Experiment 02 Detecting and Defending Against Adversarial Attacks on Machine Learning Models
├── Experiment 03 Evasion Attack on Sentiment Analysis
├── Experiment 04 ART Membership Inference Blackbox
├── Experiment 05 Model Stealing Copycat
├── Experiment 06 ART Poisoning Backdoor
├── Experiment 07 Anomalies Detection on OT pipeline
├── Experiment 08 AI Assisted Cyber Threat Intelligence
├── Experiment 09 Securing Large Language Models Against Prompt Injection
├── Experiment 10 AI Assisted Malware Reverse Engineering
├── Experiment 11 AI Assisted Forensics
└── Experiment 12 Detecting AI Powered Malware
```

---

# Author

AlphaBot42

AI Security Research  
Adversarial Machine Learning  
LLM Security  
AI for Cybersecurity
