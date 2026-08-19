<div align="center">

⭐ **If you find this work useful, consider starring the repository!**

# Securing Large Language Models Against Prompt Injection & Data Exfiltration

![SOC Cat Prompt Injection](images/soc_cat_prompt_injection.png)

**AI Security • Prompt Injection Detection • SOC Analytics • LLM Defense**

</div>

## Overview

This notebook is part of **Experiment 04 — Securing Large Language Models Against Prompt Injection and Data Exfiltration**.

The goal of **04C** is to move from offensive prompt-injection and RAG-hijacking examples to a first detection workflow.

This is a compact educational proof of concept. It does not claim to provide a production-grade detector. It shows how a simple detection pipeline behaves, where it helps, and where it remains insufficient.

The main security lesson is clear: detection is useful, but it is not enough. A secure LLM application also needs input controls, access control, context filtering, output checks, logging, and incident-response logic.

## Notebook

```text
04c_Attack_Detection_RAG_Hijacking.ipynb
```

## What this experiment does

The notebook demonstrates a simple prompt-injection detection workflow:

1. Build a small handcrafted dataset of benign prompts and injection prompts.
2. Explore label distribution and prompt length.
3. Train a baseline detector with TF-IDF and Logistic Regression.
4. Review misclassified examples.
5. Compare the baseline with a Hugging Face text-classification model.
6. Test adversarial prompt examples.
7. Apply basic preprocessing.
8. Compare the results before and after preprocessing.
9. Summarize the security takeaway.

## Dataset used in this notebook

This 04C notebook uses a small handcrafted dataset directly inside the notebook.

It is intentionally small because the objective is to explain the detection logic and its limits, not to present a large benchmark.

The larger SOC-enriched dataset is prepared separately under:

```text
Dataset_SOC/
```

That larger dataset is intended for the follow-up SOC and incident-response work in **04D**.

## Model approach

The notebook compares two detection approaches.

### Baseline model

```text
TF-IDF + Logistic Regression
```

This baseline is simple, transparent, and useful for understanding what lexical detection can and cannot capture.

### Hugging Face classifier

The notebook also tests a Hugging Face text-classification pipeline:

```text
deepset/deberta-v3-base-injection
```

This comparison is useful to show how a pretrained classifier behaves on the same prompt examples.

## Security takeaway

The experiment highlights four important points:

- Detection models can identify obvious prompt-injection attempts.
- Adversarial prompts can still bypass detection.
- Preprocessing can help against noisy text, but not against semantic attacks.
- Detection is necessary, but not sufficient.

In a real LLM application, detection must be combined with architectural controls. The model should not be the only security boundary.

## Relationship with 04D

**04C** focuses on detection.

It is intentionally compact: the notebook uses a small handcrafted dataset to make the detection workflow easy to inspect and reproduce.

**04D** extends this work toward SOC and incident response:

```text
Detection → Triage → Evidence → Containment → Incident report
```

04D is where prompt-injection events are transformed into security events that can be reviewed, prioritized, and escalated by a SOC or incident-response team.

The objective is not to claim that 04C alone is production-ready. The objective is to show the progression from a small detection proof of concept to a larger SOC-oriented response pipeline.

### 04D SOC dataset

The follow-up 04D work uses a larger SOC-enriched dataset built separately under:

```text
Dataset_SOC/
```

Current professional dataset version:

```text
pro_v3_1
```

Dataset summary:

- 250000 rows
- 23 columns
- 175000 benign events
- 75000 malicious or suspicious prompt events
- 30% target injection ratio
- Severity levels: INFO, MEDIUM, HIGH
- 63869 HIGH alerts
- 11131 MEDIUM alerts

### 04D dataset sources

The 04D dataset combines LLM prompt data with SOC, system-log, and network-security context.

LLM prompt sources:

- Anthropic HH RLHF
- deepset prompt injections
- lmsys/toxic-chat
- markush1 LLM Jailbreak Classifier, when Hugging Face access is available

SOC and network-security sources:

- Loghub 2.0
- UNSW NB15
- CICIDS2017
- Cybersecurity Threat Detection Logs

The larger dataset is used to support the 04D SOC response workflow: severity assignment, alert generation, evidence preservation, containment recommendation, and incident-report generation.

## Requirements

The notebook uses Python and common data-science / machine-learning libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn transformers torch
```

The Hugging Face model may require internet access during the first run, unless it is already available in the local cache.

## How to run

From the 04C folder:

```bash
cd "Prompt_Injection_Detection_Engine"
jupyter notebook 04c_Attack_Detection_RAG_Hijacking.ipynb
```

Or execute it from the command line:

```bash
jupyter nbconvert \
  --to notebook \
  --execute 04c_Attack_Detection_RAG_Hijacking.ipynb \
  --output 04c_Attack_Detection_RAG_Hijacking_executed.ipynb \
  --ExecutePreprocessor.timeout=-1
```

## Files

```text
Prompt_Injection_Detection_Engine/
├── 04c_Attack_Detection_RAG_Hijacking.ipynb
├── README_04C.md
├── SOC-Analyst.png
└── images/
    └── soc_cat_prompt_injection.png
```

## Limitations

This notebook is intentionally small and pedagogical.

The results should not be interpreted as a production benchmark. The dataset used in 04C is too small for that. The value of the experiment is to make the detection workflow visible and to show why a detector alone cannot secure an LLM application.

Production work would require a larger dataset, adversarial testing, multilingual examples, domain-specific prompts, threshold calibration, false-positive analysis, false-negative analysis, logging, monitoring, and incident-response integration.

That production-oriented direction is covered by the follow-up 04D work, which moves from detection to SOC-ready incident response.

## License

The code written for this experiment is released under the MIT License.

External datasets, pretrained models, and third-party resources remain subject to their own licenses and usage conditions. They are referenced for research and educational purposes and should be checked before redistribution or production use.


