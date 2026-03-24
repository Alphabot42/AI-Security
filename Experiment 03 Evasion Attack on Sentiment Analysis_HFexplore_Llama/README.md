<p align="center">
  ⭐ <b>If you find this work useful, consider starring the repository!</b>
</p>

# Adversarial Evasion Attacks on Sentiment Analysis

<p align="center">
  <img src="Evasion Attack on huggingface Model/attack_vs_defense.png" width="900">
</p>

<p align="center">
  <b>From surface robustness to semantic failure in NLP models</b>
</p>

<p align="center">
  🚨 Robust to noise. Fragile to meaning.
</p>

---

## Overview

This project explores **adversarial evasion attacks on sentiment analysis systems**, focusing on how small input perturbations can destabilize model predictions.

The key insight:

> NLP models are not truly robust  
> they are only robust to **syntax**, not **meaning**

---

## Experiments

### 03a — Hugging Face model

📁 `Evasion Attack on huggingface Model/`

- Transformer-based sentiment classifier
- Progressive attack pipeline:
  - surface perturbations (typos, casing, punctuation)
  - semantic perturbations (negation, contradiction)
  - targeted attacks (forced sentiment override)

➡️ Demonstrates:
- confidence degradation before failure
- robustness to noise
- vulnerability to semantic manipulation

---

### 03b — LLM-based model (coming soon)

📁 `Evasion Attack on llama LLM/`

- Local LLM (via Ollama)
- Same adversarial framework applied to generative models

➡️ Goal:
- compare robustness between:
  - classifier models
  - instruction-following LLMs

---

## Key Findings

- Surface perturbations have limited impact
- Confidence drops before prediction flips
- Semantic attacks can fully override model outputs
- Preprocessing defenses provide only superficial robustness

---

## Project Structure

```
Experiment 03/
├── Evasion Attack on huggingface Model/
│   ├── notebook (.ipynb)
│   ├── report (.pdf)
│   ├── README.md
│   └── attack_vs_defense.png
│
├── Evasion Attack on llama LLM/
│   └── (coming soon)
│
└── README.md  ← (this file)
```

---

## Why this matters

In real-world systems, sentiment analysis is used for:

- content moderation
- customer support triage
- brand monitoring
- decision automation

If an attacker can manipulate meaning while preserving readability:

> they can manipulate the entire downstream pipeline

---

## Next steps

- Extend attacks to LLMs (Experiment 03b)
- Evaluate robustness across architectures
- Explore semantic-aware defenses

---

## Author

Natacha Bakir  
AI Security Researcher — Malware & Threat Intelligence
