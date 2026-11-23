# Reproduce the V1 findings

## Availability

The executed notebook 04 records successful technical reproduction in my lab environment (Cube-AI)
with Python 3.11.15. The current checkout includes source code, the updated report
and table-level QA summaries. **The exact frozen runtime, full verification JSON
and input fixtures are pending transfer from that successful run.**

The preparation bundle originally supplied for QA contained helpers, not model
weights. It must not be described as a standalone trained-model download.

The recorded successful run is:

~~~text
outputs/quishing04/qa_20261122T140752771854Z/
~~~

The source EXP08 run is:

~~~text
outputs/quishing02/frozen_candidates/
  characters_structure_20261121T102606292955Z/normalized_revision/
  exp08_repeated_training_20261121T170229937001Z/
~~~

Directory names identify exact historical runs. The discovery helpers stop if a
selection is missing or ambiguous. A new research run needs explicit overrides;
silently taking the latest run would mix evidence.

## Collect the completed run in the lab environment

From the experiment directory, run the supplied standard-library collector:

~~~bash
python scripts/export_quishing_v1_evidence.py
~~~

Alternatively download the standalone script into that directory and run:

~~~bash
python export_quishing_v1_evidence.py
~~~

It verifies the completed QA report, both process-result hashes, package hashes,
source checkpoints and research evidence before creating
quishing_v1_verified_evidence.zip. It includes selected source artifacts with
their original relative paths and the split manifest when present. It excludes
the installed virtual environment, caches and the original raw dataset archive.
It does not fit models, select thresholds or contact encoded destinations.

The collector fails if the target ZIP already exists. Choose another output name
with --output when needed. Transfer the resulting archive for the final artifact
review; do not substitute a recreated or refitted checkpoint for the verified one.

## Frozen inference after artifact transfer

The successful package directory contains config.json, three model_seed_*.joblib
files, importable feature/decoder/pipeline modules, pinned requirements, lineage,
hashes and a verification directory. Use a Python 3.11 interpreter.

~~~bash
python3.11 -m venv .venv-quishing
.venv-quishing/bin/python -m pip install -r /absolute/path/to/package/requirements.txt
cd /absolute/path/to/package
/absolute/path/to/.venv-quishing/bin/python -I run_verification.py --output /absolute/path/to/replay.json --require-venv
~~~

For the same transformed subset as the original isolated-environment check,
add --transform-limit 16. Without this flag the verifier evaluates all 1,956
images under each transformation.

Individual local inference, from the package directory:

~~~python
from quishing_pipeline import analyse_png
result = analyse_png("example.png", seed=42)
print(result)
~~~

Prediction 1 is phishing, 0 is legitimate and -1 is abstention. Only the evaluated
69 × 69 grayscale display convention is supported. The decoder does not visit
the URL. Use exact stored thresholds, not rounded report values. Serialized
models must come from a trusted origin; a matching hash detects alteration
relative to a manifest but does not establish trustworthy provenance.

## Recreate the QA export

Keep qa_support beside notebook 04 at the experiment root and restore the
selected outputs/quishing02 directories. Open a fresh research kernel and run
the notebook in order. The recorded input counts are checked explicitly:
1,956 clean PNGs, 69 known-attack PNGs and 755 retained URL pairs.

Notebook 04 creates another run directory and fresh environment. Its final
comparison checks both runs against each other and the original saved evidence.
This repeats frozen inference, not full research training.

## Revisit the full research

Obtain the original QuishingDataset.zip from the authors' repository linked in
ATTRIBUTION.md. Its two pickle arrays are placed under data:

~~~text
data/qr_codes_29.pickle
data/qr_codes_29_labels.pickle
data/qr_splits_seed42.csv
~~~

Pickles, like joblib files, must be loaded only from a trusted source.
Use the exact original split manifest for historical parity. A new random or
domain partition is a different experiment.

Notebook 02 includes notebook 01's 224-cell history before the added research.
Do not execute both histories consecutively expecting the second to be a short
continuation. Source cells reference earlier local checkpoints and saved stage
outputs; select the intended research stage with its prerequisites.

The source environment reported PyTorch 2.5.1+cu121 and an RTX 2070. Exact inference
versions are in requirements-inference.txt. requirements-notebooks.in lists
additional research tools and is explicitly **not** a complete archived research
environment. Optional URLBERT weights were unavailable and must not be replaced
by random initialization presented as pretrained performance.

## Interpreting parity

Scores compare with rtol 1e-10 and atol 1e-12. Payload identity, acceptance and
classification decisions must match exactly. Hashes and counts detect wrong
inputs. The isolated-environment check is on the same host and Python major/minor
version. It does not establish portability to every machine or a new independent
performance estimate.

No measured total notebook duration is available in the supplied execution
outputs. Initial time estimates must not be republished as measured runtimes.
