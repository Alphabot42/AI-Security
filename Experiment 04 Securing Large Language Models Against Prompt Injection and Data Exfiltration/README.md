<p align="center">
  ⭐ <b>If you find this work useful, consider starring the repository!</b>
</p>

<h1 align="center">Securing Large Language Models Against Prompt Injection & Data Exfiltration</h1>

<p align="center">
  <img src="Cat_inject.png" width="900">
</p>

<p align="center">
  <i>Understanding and mitigating prompt injection attacks in LLM systems</i>
</p>

---

## Overview

This parent folder contains the Experiment 04 series focused on securing Large Language Models against prompt injection and data exfiltration attacks.

The goal is to simulate realistic attack scenarios and evaluate defensive strategies in LLM-based systems.

---

## Research Focus

This experiment explores:

- Prompt injection attacks
- Instruction override techniques
- Data exfiltration risks
- Defense mechanisms for LLM pipelines

Key question:

> How can an attacker manipulate model behavior using only crafted input?

---

## How to run

Activate the global environment:

```bash
conda activate Env_Req_global_conda
```

Then run the notebooks inside each experiment folder.

---

## Experiments

### 04A — [Prompt Injection Defense — RAG / Bank scenario](RAG_Prompt_Injection_Attack_Defense_Demo_Bank)

- Simulated sensitive environment in a banking context
- Injection through retrieved documents
- RAG hijacking scenario
- Evaluation of model behavior under adversarial prompts

---

### 04B — [Prompt Injection on LLM — Mistral banking assistant](RAG_Prompt_Injection_Attack_Defense_Demo_Mistral)

- Local Mistral assistant executed through Ollama
- Direct prompt manipulation
- Instruction override attacks
- Vulnerable banking-assistant behavior
- First hardened version and comparative analysis of model robustness

---

### 04C — [Prompt Injection Detection Engine](Prompt_Injection_Detection_Engine)

- Compact detection proof of concept
- Small handcrafted dataset of benign and prompt-injection examples
- TF-IDF and Logistic Regression baseline
- Hugging Face prompt-injection classifier comparison
- Adversarial examples and detection limitations
- Security takeaway: detection is necessary, but not sufficient

---

### 04D — [Prompt Injection Response System](Prompt_injection_Response_System)

- SOC-oriented extension of the detection workflow
- Larger SOC-enriched dataset prepared under `Dataset_SOC/`
- Prompt-injection events transformed into security alerts
- Triage, severity assignment, evidence preservation and containment recommendation
- Incident-report generation for SOC and incident-response workflows
---

## Key Insight

LLMs do not fail due to malformed inputs.

They fail because they follow instructions too well.

Prompt injection exploits this behavior by embedding malicious intent within seemingly valid inputs.

---

## Why it matters

In real-world applications:

- LLMs interact with untrusted data
- Inputs may be adversarial by design
- Sensitive information can be indirectly exposed

This creates critical risks for:

- RAG systems
- AI assistants
- Enterprise AI workflows

---

## Author

Natacha Bakir  
AI Security Researcher
