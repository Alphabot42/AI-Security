# Frozen R2 QR phishing research package

Use Python with the same major and minor version as the recorded source interpreter.
Install requirements.txt in a new virtual environment. No model fitting is required.

```python
from quishing_pipeline import analyse_png
result = analyse_png("example.png", seed=42)
print(result)
```

Only the evaluated 69 x 69 grayscale display convention is supported.
Prediction -1 means abstention, 0 legitimate, 1 phishing. Abstention must not authorize a destination.
Only accepted decoded text reaches the classifier. No destination is contacted.
Scores are not calibrated probabilities. Validation was repeatedly inspected in development.
Three seeds use one fixed split; no general robustness or production-readiness claim is made.

The separate verification directory includes historical QR payloads, including phishing addresses.
Review dataset permissions and publication inputs before sharing those fixtures.
Only load model files from a trusted origin. Hashes detect changes, not malicious provenance.
This package verifies frozen-model inference; full research training is not rerun here.
