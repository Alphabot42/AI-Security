# Reproduce the V1 findings

## Published artifacts

The portable R2 package is published as individual files in
[models/quishing_v1](../models/quishing_v1/). It contains three fitted models,
importable feature/decoder/pipeline modules, exact thresholds, pinned dependencies,
lineage, SHA-256 values and the complete frozen-inference verification inputs.

The original [split manifest](../data/qr_splits_seed42.csv), historical research
checkpoints and supporting evidence under `outputs/quishing02/`, and
[full notebook 04 verification results](../evidence/quishing_v1/lab/) are included.
The [publication layout](../evidence/quishing_v1/publication_layout.json) records
the relocation of the exported package and the original transfer manifest.

Technical reproduction originally passed in my lab environment (Cube-AI) with
Python 3.11.15. A subsequent isolated Python 3.12.14 replay with the same pinned
dependency versions matched all 21,723 original image results exactly, including
payload hashes, acceptance, decisions and scores. It also verified 755 URL pairs
for each of the three models. This documents those two environments, not arbitrary portability.

## Replay frozen inference

From the Experiment 14 directory, use Python 3.11, the original interpreter series:

~~~bash
python3.11 -m venv .venv-quishing
.venv-quishing/bin/python -m pip install -r models/quishing_v1/requirements.txt
.venv-quishing/bin/python -I models/quishing_v1/run_verification.py --output outputs/quishing_v1_replay.json --require-venv
~~~

The verifier checks package hashes before inference. It replays all 1,956 clean
and 69 known-attack PNGs for seeds 42, 142 and 242; 755 URL pairs per seed; and
eight image transformations over the entire 1,956-image cohort with seed 42.
No model fitting or threshold calibration is performed.

For the fixed transformed subset used in the original isolated-environment check,
add `--transform-limit 16`. The clean and known-attack cohorts and URL pairs are
still replayed completely. Without that flag the result contains 21,723 image records.

The original lab isolated check used the subset. The independent post-transfer
review replayed the complete transformation suite. See the
[verification receipt](../evidence/quishing_v1/artifact_verification.json) and
[independent results](../evidence/quishing_v1/independent_replay.json).

For individual inference, run this Python from `models/quishing_v1/`:

~~~python
from quishing_pipeline import analyse_png
result = analyse_png("verification/images/clean/5.png", seed=42)
print(result)
~~~

Prediction 1 is phishing, 0 legitimate and -1 abstention. Only the evaluated
69 × 69 grayscale convention is supported. The decoder does not visit the URL.
Inference uses full stored thresholds. Serialized models must come from a trusted
origin; a matching hash detects changes relative to a manifest, not trustworthy provenance.

## Recreate the notebook 04 export

Keep `qa_support` beside notebook 04 at the experiment root. The selected source
checkpoints and evidence retain the following dated layout:

~~~text
outputs/quishing02/frozen_candidates/
  characters_structure_20261121T102606292955Z/normalized_revision/
  exp08_repeated_training_20261121T170229937001Z/
~~~

Use a fresh research kernel and the prerequisites documented in notebook 04.
Discovery helpers stop if the required historical run is missing or ambiguous;
silently selecting a newer run would mix evidence.
The notebook creates a new export run directory and isolated environment.
This repeats frozen inference and export, not full research training.

Original notebook 04 run-level outputs are now in
`evidence/quishing_v1/lab/`; its portable package is in `models/quishing_v1/`.
Interpreter paths recorded in those JSON files describe the original machines.

## Revisit the full research

Obtain the original `QuishingDataset.zip` from the authors' repository linked in
[ATTRIBUTION.md](ATTRIBUTION.md). Place its two pickle arrays under `data`:

~~~text
data/qr_codes_29.pickle
data/qr_codes_29_labels.pickle
data/qr_splits_seed42.csv
~~~

The exact original split manifest is included. A new random or domain partition
is a different experiment. Pickle and joblib files must come from a trusted source.

Notebook 02 includes notebook 01's 224-cell history before the added research.
Do not execute both histories consecutively expecting a short continuation.
Research cells also use earlier checkpoints and saved stages: select the intended
stage and its prerequisites. The raw dataset archive is obtained from its authors.

The source research environment reported PyTorch 2.5.1+cu121 and an RTX 2070.
`requirements-notebooks.in` lists additional tools; it is not a complete archived
research environment. Exact frozen-inference versions are supplied in the model
package. Optional URLBERT weights were unavailable and must not be replaced by
random initialization described as pretrained performance.

## Interpreting parity

Score checks use rtol 1e-10 and atol 1e-12; the independent complete replay
observed a maximum difference of zero. Payload identity, acceptance and decisions
matched exactly. Gaussian blur sigma 1.0 reproduced 1,956 abstentions.

These checks reuse the recorded, previously inspected V1 validation data. They
do not establish independent generalization or repeat adaptive attack discovery.
The original same-host isolated installation and the later independent replay
are separate verification events. No measured total notebook duration is asserted.
