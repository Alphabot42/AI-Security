"""Recalculate predictions and verify saved evidence without a research notebook."""
import argparse
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import platform
import site
import sys
import time
import numpy as np
import quishing_features as features
from quishing_pipeline import (ROOT, CONFIG, get_model, threshold, read_png_pixels,
    decode_pixels, analyse_decoded, transform_pixels, n02_png)

TRANSFORMS = ['rotate_90', 'rotate_180', 'rotate_270', 'jpeg_90', 'jpeg_60',
              'blur_0.5', 'blur_1.0', 'contrast_0.65']

def hash_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def close(actual, expected, context):
    if not np.isclose(float(actual), float(expected), rtol=1e-10, atol=1e-12):
        raise AssertionError(f'Score mismatch for {context}: {actual} vs {expected}')

def verify_files():
    hashes = json.loads((ROOT / 'sha256.json').read_text())
    for name, expected in hashes.items():
        file = ROOT / name
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Package integrity mismatch: {name}')

def run(output, transform_limit=0, require_venv=False):
    started = time.perf_counter()
    verify_files()
    boundaries = [
        ('EXAMPLE.com/%6Cogin?x=%61#%62', 'example.com/login?x=%61#%62', True),
        ('https://EXAMPLE.com/a%2Fb/%252F', 'https://example.com/a%2Fb/%252F', True),
        ('example.com/%2E%2E/login', 'example.com/../login', True),
        ('EXAMPLE.com/bad%2', 'EXAMPLE.com/bad%2', False),
    ]
    for raw, expected, supported in boundaries:
        if features.n02_normalize_host_path_one(raw) != (expected, supported):
            raise AssertionError('Normalization boundary behaviour changed.')
    if require_venv:
        if sys.prefix == sys.base_prefix:
            raise AssertionError('Fresh-environment verification requires a virtual environment.')
        cfg = Path(sys.prefix) / 'pyvenv.cfg'
        if not cfg.is_file() or 'include-system-site-packages = false' not in cfg.read_text().lower():
            raise AssertionError('Virtual environment must not inherit system site-packages.')
    plan = json.loads((ROOT / 'verification/plan.json').read_text())
    seeds = CONFIG['seeds']
    records = []
    for number, item in enumerate(plan['clean'], 1):
        decoded = decode_pixels(read_png_pixels(ROOT / item['file']))
        if not decoded['accepted'] or hash_text(decoded['text']) != item['payload_sha256']:
            raise AssertionError(f"Clean payload recovery mismatch: {item['image_index']}")
        for seed in seeds:
            result = analyse_decoded(decoded, seed)
            expected = item['expected'][str(seed)]
            close(result['score'], expected['score'], f"clean {item['image_index']} seed {seed}")
            if result['prediction'] != expected['prediction']:
                raise AssertionError('Clean decision mismatch.')
            records.append({'group': 'clean', 'image_index': item['image_index'],
                'seed': seed, 'label': item['label'], 'payload_sha256': hash_text(decoded['text']),
                'accepted': True, 'score': result['score'], 'prediction': result['prediction']})
        if number % 250 == 0 or number == len(plan['clean']):
            print(f"Clean QR: {number}/{len(plan['clean'])}", flush=True)
    for item in plan['attacks']:
        decoded = decode_pixels(read_png_pixels(ROOT / item['file']))
        if not decoded['accepted'] or hash_text(decoded['text']) != item['payload_sha256']:
            raise AssertionError(f"Attack payload recovery mismatch: {item['image_index']}")
        for seed in seeds:
            result = analyse_decoded(decoded, seed)
            # This is the original-source score, not a previously stored candidate score.
            close(result['score'], item['original_scores'][str(seed)],
                  f"known path-invariance replay {item['image_index']} seed {seed}")
            if result['prediction'] != 1:
                raise AssertionError('Known stored attack is no longer detected.')
            records.append({'group': 'stored_path_attack', 'image_index': item['image_index'],
                'seed': seed, 'label': 1, 'payload_sha256': hash_text(decoded['text']),
                'accepted': True, 'score': result['score'], 'prediction': result['prediction']})
    pairs = json.loads((ROOT / 'verification/path_pairs.json').read_text())
    pair_checks = []
    for seed in seeds:
        model = get_model(seed)
        original = model.predict_proba([p['original_payload'] for p in pairs])[:, 1]
        candidate = model.predict_proba([p['candidate_payload'] for p in pairs])[:, 1]
        delta = float(np.max(np.abs(original - candidate)))
        if delta != 0.0 or not (original >= threshold(seed)).all():
            raise AssertionError('Retained text-pair invariance changed.')
        pair_checks.append({'seed': seed, 'pairs': len(pairs), 'maximum_score_difference': delta,
                            'retained_pair_evasions': int(((original >= threshold(seed)) &
                                                          (candidate < threshold(seed))).sum())})
    sample = plan['clean']
    if transform_limit:
        positions = np.unique(np.linspace(0, len(sample)-1, transform_limit, dtype=int))
        sample = [sample[int(i)] for i in positions]
    for name in TRANSFORMS:
        for number, item in enumerate(sample, 1):
            pixels = transform_pixels(read_png_pixels(ROOT / item['file']), name)
            # The captured research decoder stores/quantizes PNG bytes internally.
            decoded = decode_pixels(pixels)
            result = analyse_decoded(decoded, 42)
            payload_hash = hash_text(decoded['text']) if decoded['accepted'] else None
            if decoded['accepted'] and payload_hash == item['payload_sha256']:
                close(result['score'], item['expected']['42']['score'], f'{name} exact-payload score')
                if result['prediction'] != item['expected']['42']['prediction']:
                    raise AssertionError('Exact recovered payload changed the decision.')
            records.append({'group': name, 'image_index': item['image_index'], 'seed': 42,
                'label': item['label'], 'payload_sha256': payload_hash,
                'reference_exact': bool(decoded['accepted'] and payload_hash == item['payload_sha256']),
                'accepted': decoded['accepted'], 'score': result['score'],
                'prediction': result['prediction']})
            if number % 500 == 0 or number == len(sample):
                print(f'{name}: {number}/{len(sample)}', flush=True)
    result = {'status': 'passed', 'python': sys.version, 'executable': sys.executable,
        'prefix': sys.prefix, 'base_prefix': sys.base_prefix,
        'isolated_venv_checked': bool(require_venv), 'user_site_enabled': bool(site.ENABLE_USER_SITE),
        'platform': platform.platform(), 'elapsed_seconds': time.perf_counter()-started,
        'transform_limit': transform_limit, 'records': records, 'pair_checks': pair_checks,
        'versions': {name: metadata.version(name) for name in CONFIG['distributions']}}
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(f'Verification passed; results saved to {output.name}', flush=True)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--transform-limit', type=int, default=0)
    parser.add_argument('--require-venv', action='store_true')
    args = parser.parse_args()
    run(args.output, args.transform_limit, args.require_venv)
