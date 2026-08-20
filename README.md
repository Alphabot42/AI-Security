
# AI Security Research Projects
### Adversarial Machine Learning | LLM Security | AI for Cybersecurity

This repository contains a collection of practical AI security research projects exploring adversarial machine learning, large language model security, and the application of AI techniques to cybersecurity domains such as cyber threat intelligence, malware analysis, and digital forensics.

The objective of these experiments is to understand how machine learning systems can be attacked, manipulated, and defended in real-world scenarios. Many experiments are mapped to the OWASP Top 10 Risks for LLM Applications to align with modern AI security practices.

This repository is structured as a progressive research roadmap, starting from adversarial ML fundamentals and advancing toward applied AI security use cases.

---

<p align="center">
  ⭐ If you find this work useful, consider starring the repository!
</p>

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
| Phase                              | Experiment                                         | Notebook  /Material                  | OWASP AI Top 10                        | Skills                             | Progress        |
|-----------------------------------|-----------------------------------------------------|--------------------------------------|----------------------------------------|------------------------------------|-----------------|
| Phase 1 – Adversarial ML          | Practical Adversarial Attacks on Vision Models      | adversarial_samples_cifar10_demo     | LLM02 Insecure Output Handling         | Offensive AI Security              | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02 LLM security series               | LLM02 Insecure Output Handling         | Offensive / Defensive AI Security  | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02b pretrained variant               | LLM02 Insecure Output Handling         | Offensive / Defensive AI Security  | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02c HF optimized                     | LLM04 Model Denial of Service          | Offensive / Defensive AI Security  | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02d HF detector 16 threads           | LLM09 Overreliance                     | Offensive / Defensive AI Security  | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02e train detector MNIST             | LLM09 Overreliance                     | Offensive / Defensive AI Security  | ██████████ 100% |
| Phase 1 – Adversarial ML          | Detecting and Defending Against Adversarial Attacks | 02f input transform defense          | LLM09 Overreliance                     | Offensive / Defensive AI Security  | ██████████ 100% |
| Phase 2 – Modern Models (LLM)     | Evasion Attack on Sentiment Analysis                | 03a HFexplore_ evasion attack        | LLM01 Prompt Injection, LLM06 SID      | Offensive / Defensive AI Security  | ██████████ 100% |
| Phase 2 – Modern Models (LLM)     | Evasion Attack on Sentiment Analysis                | 03b Llama evasion attack             | LLM01 Prompt Injection, LLM06 SID      | Offensive / Defensive AI Security  | ██████████ 100% |
| Phase 2 – Modern Models (LLM)     | Securing LLMs Against Prompt Injection              | 04a Attack_Defense_RAG_Hijacking     | LLM01 Prompt Injection, LLM06 SID      | Defensive AI Security              | ██████████ 100% |
| Phase 2 – Modern Models (LLM)     | Securing LLMs Against Prompt Injection              | 04b Mistral prompt injection defenses| LLM01 Prompt Injection, LLM06 SID      | Defensive AI Security              | ██████████ 100% |
| Phase 2 – Modern Models (LLM)     | Securing LLMs Against Prompt Injection              | 04c Prompt Injection Detection Engine | LLM01 Prompt Injection, LLM06 SID      | Defensive AI Security / Detection Engineering | ██████████ 100% |
| Phase 2 – Modern Models (LLM)     | Securing LLMs Against Prompt Injection              | 04d SOC/IR Prompt Injection Response System | LLM01 Prompt Injection, LLM06 SID, LLM08 Excessive Agency | Defensive AI Security / SOC / Incident Response | ██████████ 100% |
| Phase 3 – Training Pipeline       | Membership Inference (Blackbox)                     | ART membership inference             | LLM06 Sensitive Information Disclosure | Offensive AI Security              | ██░░░░░░░░ 25%  |
| Phase 3 – Training Pipeline       | Model Stealing (Copycat)                            | model extraction attack              | LLM10 Model Theft                      | Offensive AI Security              | █░░░░░░░░░ 10%  |
| Phase 3 – Training Pipeline       | Training Data Poisoning (Backdoor)                  | ART poisoning attack                 | LLM03 Training Data Poisoning          | Offensive AI Security              | █░░░░░░░░░ 10%  |
| Phase 4 – Defense Systems         | Anomaly Detection on OT Pipeline                    | OT anomaly detection                 | LLM08 Excessive Agency                 | DPM / DS / ML / MLOps              | ████████░░ 75%  |
| Phase 4 – Defense Systems         | SecMLOps                                            | Airflow Weather Pipeline             | LLM03 Training Data Poisoning, LLM06 SID, LLM08 Excessive Agency| SecMLOps  | ██░░░░░░░░ 25%  |
| Phase 5 – AI for Cybersecurity    | AI Assisted Cyber Threat Intelligence               | 09a Secure AI CTI Assistant          | LLM06 SID, LLM07 Plugin Design         | Defensive AI Security              | ██████████ 100% |
| Phase 5 – AI for Cybersecurity    | AI Assisted Cyber Threat Intelligence               | 09b AI CTI Assistant on AWS          | LLM06 SID, LLM07 Plugin Design         | Defensive AI Security              | ██████████ 100% | 
| Phase 5 – AI for Cybersecurity    | AI Assisted Cyber Threat Intelligence               | 09c malware adversary tracking       | LLM06 SID, LLM07 Plugin Design         | Defensive AI Security              | █░░░░░░░░░ 10%  |
| Phase 5 – AI for Cybersecurity    | AI Assisted Malware Reverse Engineering             | 09d AI malware deobfuscation         | LLM06 SID, LLM07 Plugin Design         | Defensive AI Security              | ░░░░░░░░░░ 0%   |
| Phase 5 – AI for Cybersecurity    | AI Assisted Forensics                               | 09e AI forensic investigation        | LLM06, LLM02, LLM08, LLM07             | Defensive AI Security              | ░░░░░░░░░░ 0%   |
| Capstone                          | Detecting AI Powered Malware                        | 10 AI malware detection system       | LLM08 Excessive Agency, LLM02 IOH      | Defensive AI Security              | ░░░░░░░░░░ 0%   |

---

# OWASP AI Top 10 Coverage

| OWASP Risk | Covered Experiments |
|-------------|--------------------|
| LLM01 Prompt Injection | LLM Evasion Attacks, Prompt Injection Defense |
| LLM02 Insecure Output Handling | Adversarial ML Attacks |
| LLM03 Training Data Poisoning | Backdoor Poisoning, SecMLOps Airflow Weather Pipeline |
| LLM04 Model Denial of Service | Adversarial Input Attacks |
| LLM06 Sensitive Information Disclosure | Membership Inference, SecMLOps Airflow Weather Pipeline |
| LLM07 Insecure Plugin Design | AI Cybersecurity Tooling |
| LLM08 Excessive Agency | Autonomous Detection Systems, SecMLOps Airflow Weather Pipeline |
| LLM09 Overreliance | Adversarial Detection |
| LLM10 Model Theft | Model Stealing Attacks |

---




# Repository Structure

```text
AI-Security
│
├── 0-Practical Adversarial Attacks on Vision Models FGSM Attack on CIFAR 10 using ART
│
├── Experiment 01 Adversarial Examples in Practice Breaking a Vision Model with FGSM
│   ├── env/
│   ├── 01_LLM_Security_series_adversarial...
│   └── README_Experiment_01.md
│
├── Experiment 02 Detecting and Defending Against Adversarial Attacks on Machine Learning Models
│   ├── 02_LLM_security_series-Attack_Defense_...
│   ├── 02_Requirements_files/
│   ├── 02b_Pretrained_model_variant/
│   ├── 02c_Defending_Against_Adversarial_...
│   ├── 02d_Defending_Against_Adversarial_...
│   ├── 02e_Train_a_detector_on_MNIST_...
│   ├── 02f_Input_Transform/
│   ├── data/MNIST/raw/
│   ├── README.md
│   ├── cover_experiment_02.png
│   ├── adv_training_improvement.png
│   ├── detector_performance.png
│   └── robustness_curve.png
│
├── Experiment 03 Evasion Attack on Sentiment Analysis_HFexplore_Llama
│   ├── Evasion Attack on huggingface Models
│   ├── Evasion Attack on llama LLM
│   ├── README.md
│   └── cover_experiment_03.png
│
├── Experiment 04 Securing Large Language Models Against Prompt Injection and Data Exfiltration
│   ├── RAG_Prompt_Injection_Attack_Defense_Demo_Bank/
│   │   └── 04A — RAG hijacking attack scenario in a banking context
│   │
│   ├── RAG_Prompt_Injection_Attack_Defense_Demo_Mistral/
│   │   └── 04B — Vulnerable and hardened Mistral banking assistant
│   │
│   ├── Prompt_Injection_Detection_Engine/
│   │   └── 04C — Prompt-injection detection engine
│   │
│   ├── Prompt_Injection_Response_System/
│   │   └── 04D — Public SOC/IR response showcase
│   │
│   ├── Cat_inject.png
│   └── README.md
│
├── Experiment 08 Anomalies Detection on OT pipeline
│
├── Experiment 09 AI Assisted Cyber Threat Intelligence
│
├── Experiment 13 SecMLOps Airflow Weather Pipeline
│   ├── dags/
│   ├── docs/
│   ├── sample_data/
│   ├── screenshots/
│   ├── .gitignore
│   ├── README.md
│   ├── README_SCREENSHOTS.md
│   ├── SECURITY.md
│   ├── docker-compose.yaml
│   └── variables.example.json
│
├── .gitattributes
├── AI-Tools.csv
├── AI_security_baseline_checklist.docx
├── AI_security_baseline_checklist.md
├── Claude_Guide.jpg
├── open-source for pentest ML-AI.txt
└── README.md
```
---

# Author

AlphaBot42

AI Security Research  
Adversarial Machine Learning  
LLM Security  
AI for Cybersecurity
