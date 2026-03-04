# Experiment 01 — Adversarial Examples in Practice
## Breaking a Vision Model with FGSM

### Overview
This notebook introduces the fundamentals of adversarial machine learning by demonstrating how small, carefully crafted perturbations can cause deep learning vision models to misclassify images.

Using the CIFAR-10 dataset and a baseline CNN model, we generate adversarial examples with the Fast Gradient Sign Method (FGSM) and analyze how model predictions change under attack.

### Objectives
- Train a baseline CNN classifier on CIFAR-10
- Implement FGSM adversarial attack
- Visualize adversarial perturbations
- Measure classification degradation caused by adversarial inputs
- Introduce the concept of robustness evaluation

### Key Concepts
- Gradient-based adversarial attacks
- Perturbation magnitude (epsilon)
- Confidence degradation
- Adversarial robustness baseline measurement

### Output
The notebook produces:
- Clean accuracy results
- Adversarial accuracy under FGSM
- Visual comparisons of clean vs adversarial samples

### Position in Research Series
This experiment introduces adversarial example generation and establishes the baseline model that will later be used for robustness evaluation and defense research in subsequent experiments.

### Next Experiment
Experiment 02 — Detecting and Defending Against Adversarial Attacks on Machine Learning Models
