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

### 04a — Prompt Injection Defense (RAG / Bank scenario)

- Simulated sensitive environment (bank context)
- Injection through retrieved documents
- Evaluation of model behavior under adversarial prompts

---

### 04b — Prompt Injection on LLM (Mistral)

- Direct prompt manipulation
- Instruction override attacks
- Comparative analysis of model robustness

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
