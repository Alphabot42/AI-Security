"""Collect the completed Cube-AI run for publication without running models."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


RUN_NAME = "qa_20261122T140752771854Z"
RESEARCH_RUN = "exp08_repeated_training_20261121T170229937001Z"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(root: Path, path: Path) -> Path:
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError(f"File is outside the experiment directory: {path}")
    if path.is_symlink():
        raise ValueError(f"Symbolic link is not collected: {path}")
    return resolved


def unique(candidates, description: str) -> Path:
    candidates = sorted(set(candidates))
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one {description}; found {len(candidates)}. "
            "Select the intended run explicitly instead of mixing runs."
        )
    return candidates[0]


def collect(project: Path, run: Path, output: Path) -> dict:
    """Verify the recorded hashes, then collect files into a new archive."""
    project = project.resolve(strict=True)
    run = inside(project, run)
    package = run / "package"
    report = read_json(run / "qa_report.json")
    if report.get("technical_status") != "passed":
        raise ValueError("The selected QA run did not pass.")
    expected_scope = {
        "clean_QRs_per_seed": 1956,
        "known_path_attack_QRs_per_seed": 69,
        "retained_path_pairs_per_seed": 755,
        "R2_full_transformations_seed_42": 8,
        "fresh_transformations_samples_per_condition": 16,
    }
    if any(report.get(key) != value for key, value in expected_scope.items()):
        raise ValueError("The QA report has a different verification scope.")
    if report.get("seeds") != [42, 142, 242]:
        raise ValueError("The QA report has different training seeds.")

    same_path = run / "same_environment_results.json"
    fresh_path = run / "fresh_environment_results.json"
    for path, key in [
        (same_path, "same_environment_result_sha256"),
        (fresh_path, "fresh_environment_result_sha256"),
    ]:
        if digest(path) != report[key]:
            raise ValueError(f"QA report hash mismatch: {path.name}")
        if read_json(path).get("status") != "passed":
            raise ValueError(f"Verification did not pass: {path.name}")
    fresh = read_json(fresh_path)
    if not fresh.get("isolated_venv_checked"):
        raise ValueError("The fresh environment was not verified.")

    selected: dict[str, Path] = {}

    def add(path: Path):
        checked = inside(project, path)
        selected[checked.relative_to(project).as_posix()] = checked

    def add_tree(directory: Path):
        for path in sorted(directory.rglob("*")):
            relative = path.relative_to(directory)
            if any(
                part in {
                    "fresh_environment", "__pycache__", ".ipynb_checkpoints",
                    ".venv", ".git",
                }
                for part in relative.parts
            ):
                continue
            if path.is_file():
                add(path)

    hashes = read_json(package / "sha256.json")
    for name, expected in hashes.items():
        path = inside(package.resolve(), package / name)
        if digest(path) != expected:
            raise ValueError(f"Package hash mismatch: {name}")

    # Keep the exact successful run, excluding its installed virtual environment.
    add_tree(run)
    lineage = read_json(package / "artifact_lineage.json")
    research_dirs = {
        (project / item["source_checkpoint"]).parent.parent
        for item in lineage["models"]
    }
    exp08 = unique(research_dirs, "source research run")
    if exp08.name != RESEARCH_RUN:
        raise ValueError("The source run differs from the reviewed V1 run.")
    evidence_manifest = read_json(exp08 / "evidence_manifest.json")
    for item in evidence_manifest["evidence"] + evidence_manifest["models"]:
        if digest(inside(exp08.resolve(), exp08 / item["file"])) != item["sha256"]:
            raise ValueError(f"Source evidence hash mismatch: {item['file']}")
    add_tree(exp08)

    # Retain the original directory layout needed by notebooks 03 and 04.
    normalized = exp08.parent
    search = unique(
        [
            path
            for path in normalized.glob("exp13_path_encoding_*/schemeless_search")
            if (path / "stored_qr_verification/details.csv").is_file()
        ],
        "path-attack evidence directory",
    )
    add_tree(search)
    decoder = unique(
        [
            path
            for path in normalized.glob("qr_package_*")
            if (path / "qr_decoder.py").is_file()
            and (path / "sha256.json").is_file()
        ],
        "captured decoder package",
    )
    for name in ["qr_decoder.py", "sha256.json"]:
        add(decoder / name)
    decoder_hashes = read_json(decoder / "sha256.json")
    if digest(decoder / "qr_decoder.py") != decoder_hashes["qr_decoder.py"]:
        raise ValueError("The captured decoder source changed.")

    split = project / "data/qr_splits_seed42.csv"
    if split.is_file():
        add(split)

    # Archive publication inputs, not a Python environment or the raw data ZIP.
    output = output.resolve()
    if output.exists():
        raise FileExistsError(f"Refusing to replace an archive: {output}")
    if output.is_relative_to(run) or output.is_relative_to(search):
        raise ValueError("Save the archive outside the directories being collected.")
    manifest = {
        "task": "Q14_04_JAL01",
        "qa_run": run.relative_to(project).as_posix(),
        "qa_technical_status": report["technical_status"],
        "files": [
            {"file": name, "bytes": path.stat().st_size, "sha256": digest(path)}
            for name, path in sorted(selected.items())
        ],
        "upstream_dataset": {
            "authors": ["Fouad Trad", "Ali Chehab"],
            "paper": "https://arxiv.org/abs/2505.03451",
            "repository": (
                "https://github.com/fouadtrad/"
                "Detecting-Quishing-Attacks-with-Machine-Learning-Techniques-"
                "Through-QR-Code-Analysis"
            ),
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "changes": (
                "Selected and regenerated QR fixtures, transformed images, "
                "derived memberships, model outputs and experiment metadata."
            ),
        },
        "scope": (
            "Exact QA evidence and selected source artifacts; no model was "
            "trained, threshold recalibrated or destination contacted."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "x", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for name, path in sorted(selected.items()):
            archive.write(path, name)
        archive.writestr(
            "PUBLICATION_TRANSFER_MANIFEST.json",
            json.dumps(manifest, indent=2) + "\n",
        )
    with ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("Archive integrity verification failed.")
    return {
        "archive": str(output),
        "files": len(selected),
        "bytes": output.stat().st_size,
        "sha256": digest(output),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--run", type=Path)
    parser.add_argument(
        "--output", type=Path, default=Path("quishing_v1_verified_evidence.zip")
    )
    args = parser.parse_args()
    project = args.project_root.resolve()
    run = args.run or project / "outputs/quishing04" / RUN_NAME
    if not run.is_absolute():
        run = project / run
    result = collect(project, run, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
