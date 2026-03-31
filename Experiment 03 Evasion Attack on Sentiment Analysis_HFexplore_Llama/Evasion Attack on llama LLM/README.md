<p align="center">
⭐ <b>If you find this work useful, consider starring the repository!</b>
</p>

# Experiment 03b - Evasion Attack on Sentiment Analysis (LLM - LLaMA)

---

## Overview

This experiment extends 03a by replacing the Hugging Face classifier with a local LLM (LLaMA via Ollama).

The objective is to evaluate whether LLMs are more robust to adversarial evasion attacks.

---

## Objective

- Build a clean LLM-based sentiment pipeline
- Apply the same adversarial attacks as 03a
- Evaluate model behavior under attack
- Introduce defensive mechanisms
- Compare attacked vs defended performance

---

## Key Findings

- LLMs are more flexible but also introduce new failure modes
- Semantic attacks remain highly effective
- Ambiguous classes (NEUTRAL) are the most vulnerable
- Lightweight defenses provide partial mitigation
- Robust defenses introduce trade-offs

---

## Defense Strategy

We progressively introduce:

- Input normalization
- Prompt hardening
- Output constraint enforcement

This simulates a production-ready LLM security pipeline.

---

## Security Insight

LLMs do not fail in the same way as classifiers:

- They may follow injected instructions instead of preserving meaning
- They are especially vulnerable to **semantic-level manipulation**
- Robustness improvements often come at the cost of precision

---

## Key Takeaway

> Adversarial robustness in LLMs requires layered defenses, not just preprocessing.

---

## Author

Natacha Bakir  
AI Security Researcher
