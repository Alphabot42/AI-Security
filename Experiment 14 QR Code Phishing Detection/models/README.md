<p align="center">
  ⭐ <b>If you find this work useful, consider starring the repository!</b>
</p>

# Exported research models

[`quishing_v1/`](quishing_v1/) contains the frozen R2 QR phishing package: three fitted
models, inference modules, pinned requirements, hashes and verification inputs.
The package preserves the original bytes checked after notebook 04.

Use the [reproduction instructions](../docs/REPRODUCIBILITY.md) to load a model or
replay the recorded cases. The [artifact verification receipt](../evidence/quishing_v1/artifact_verification.json)
records the file checks, source checkpoint parity and independent replay.

The lab verification used Python 3.11.15. An isolated Python 3.12.14 replay with
the same pinned dependency versions matched all 21,723 recorded image results,
with no score difference. It also checked 755 URL pairs per model.
No model fitting or threshold recalibration was performed during this review.

Verification fixtures are derived from the dataset by Fouad Trad and Ali Chehab,
distributed under CC BY 4.0. See [dataset and method attribution](../docs/ATTRIBUTION.md).
The original dated research checkpoints remain under `outputs/quishing02/` for provenance;
use the portable exports in `quishing_v1/` for standalone inference.
