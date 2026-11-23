"""Inference for exported R2 checkpoints. Only accepted decoded text is classified."""
import json
from pathlib import Path
import joblib
import numpy as np
import cv2
import quishing_features
from qr_decoder import n02_decode, n02_geometry, n02_png

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
_MODELS = {}

def get_model(seed=42):
    seed = int(seed)
    if str(seed) not in CONFIG['thresholds']:
        raise ValueError(f'Unknown exported seed: {seed}')
    if seed not in _MODELS:
        _MODELS[seed] = joblib.load(ROOT / f'model_seed_{seed}.joblib')
    return _MODELS[seed]

def threshold(seed=42):
    return float(CONFIG['thresholds'][str(int(seed))])

def read_png_pixels(path):
    raw = Path(path).read_bytes()
    image = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_GRAYSCALE)
    if image is None or image.shape != (69, 69):
        raise ValueError('Expected a readable 69 x 69 grayscale image.')
    pixels = image.astype(np.float32) / 255.0
    return 1.0 - pixels if int(n02_geometry['black_value']) == 1 else pixels

def decode_pixels(pixels):
    pixels = np.asarray(pixels, dtype=np.float32)
    if pixels.shape != (69, 69) or not np.isfinite(pixels).all():
        raise ValueError('Expected finite 69 x 69 grayscale model-space pixels.')
    if pixels.min() < 0 or pixels.max() > 1:
        raise ValueError('Pixels must be within [0, 1].')
    result = n02_decode(pixels)
    text = str(result.get('text') or '')
    accepted = bool(text) and not bool(result.get('conflict', False))
    return {'text': text, 'accepted': bool(accepted),
            'conflict': bool(result.get('conflict', False))}

def analyse_decoded(decoded, seed=42):
    if not decoded['accepted']:
        return {**decoded, 'score': None, 'prediction': -1, 'status': 'abstain'}
    score = float(get_model(seed).predict_proba([decoded['text']])[0, 1])
    prediction = int(score >= threshold(seed))
    return {**decoded, 'score': score, 'prediction': prediction,
            'status': 'phishing' if prediction else 'legitimate'}

def analyse_pixels(pixels, seed=42):
    return analyse_decoded(decode_pixels(pixels), seed)

def analyse_png(path, seed=42):
    return analyse_pixels(read_png_pixels(path), seed)

def transform_pixels(pixels, name):
    if name.startswith('rotate_'):
        value = np.rot90(pixels, int(name.split('_')[1]) // 90).copy()
    elif name.startswith('jpeg_'):
        image = np.rint(np.clip(pixels, 0, 1) * 255).astype(np.uint8)
        ok, encoded = cv2.imencode('.jpg', image,
            [cv2.IMWRITE_JPEG_QUALITY, int(name.split('_')[1])])
        if not ok:
            raise RuntimeError('JPEG encoding failed.')
        restored = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
        if restored is None:
            raise RuntimeError('JPEG reload failed.')
        value = restored.astype(np.float32) / 255.0
    elif name.startswith('blur_'):
        value = cv2.GaussianBlur(pixels.astype(np.float32), (0, 0),
                                sigmaX=float(name.split('_')[1]))
    elif name == 'contrast_0.65':
        value = .65 * pixels.astype(np.float32) + .175
    else:
        raise ValueError(name)
    return np.ascontiguousarray(np.clip(value, 0, 1), dtype=np.float32)
