<p align="center">
  ⭐ <b>If you find this work useful, consider starring the repository!</b>
</p>

# Frozen V1 artifact verification

| File or folder | Purpose |
|---|---|
| [artifact_verification.json](artifact_verification.json) | Integrity checks, original/exported model state parity and independent replay summary. |
| [independent_replay.json](independent_replay.json) | Full independent results for the clean cohort, known attacks, eight transformations and URL pairs. |
| [lab/](lab/) | Original notebook 04 results, report, inventory and verification logs. |
| [transfer_manifest.json](transfer_manifest.json) | Original transfer file names, sizes and SHA-256 values. |
| [publication_layout.json](publication_layout.json) | Mapping from the original run layout to the published folders. |

The independent replay compared 21,723 image results with the original lab run.
Payload hashes, acceptance, decisions and scores matched exactly. Each model
also preserved scores across 755 original/encoded URL pairs.
Gaussian blur sigma 1.0 reproduced the documented 1,956 abstentions.

The frozen inference package is in [models/quishing_v1](../../models/quishing_v1/).
Historical source checkpoints and research evidence retain their original
relative paths under `outputs/quishing02/`. The original split manifest is
provided in [data/qr_splits_seed42.csv](../../data/qr_splits_seed42.csv).
Recorded interpreter paths describe the original machines; current run commands
are in the [reproduction guide](../../docs/REPRODUCIBILITY.md).

These checks replay the recorded V1 data. They do not constitute new-data
generalization, new training or a new adaptive attack search.
