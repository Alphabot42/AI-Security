
import json
import numpy as np
import cv2
import zxingcpp
import functools
from functools import lru_cache, cache

n02_cv = cv2.QRCodeDetector()

n02_geometry = json.loads('{"border": 0, "pitch": 1, "modules": 69, "black_value": 0, "train_fit": 1.0, "version": 13}')

def n02_png(pixels):
    # Store in display polarity using a global convention learned on train.
    model_bytes = np.rint(np.clip(pixels, 0, 1) * 255).astype(np.uint8)
    view = 255 - model_bytes if n02_geometry["black_value"] == 1 else model_bytes
    ok, encoded = cv2.imencode(".png", view)
    if not ok:
        raise RuntimeError("PNG encoding failed.")
    restored = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    assert np.array_equal(view, restored)
    model_restored = 255 - restored if n02_geometry["black_value"] == 1 else restored
    return model_restored.astype(np.float32) / 255, restored


@lru_cache(maxsize=10000)
def n02_decode_bytes(raw_bytes):
    pixels = np.frombuffer(raw_bytes, dtype=np.uint8).reshape(69, 69)
    qr = cv2.copyMakeBorder(pixels, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=255)
    qr = cv2.resize(qr, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
    try:
        cv_text, _, _ = n02_cv.detectAndDecode(qr)
    except (cv2.error, UnicodeDecodeError):
        cv_text = ""
    try:
        results = zxingcpp.read_barcodes(
            qr,
            formats=zxingcpp.BarcodeFormat.QRCode,
            try_rotate=True,
            try_downscale=True,
            try_invert=True,
            text_mode=zxingcpp.TextMode.Plain,
        )
        zx_values = sorted({r.text for r in results if r.valid and r.text})
    except (RuntimeError, UnicodeDecodeError):
        zx_values = []
    values = set(zx_values) | ({cv_text} if cv_text else set())
    text = next(iter(values)) if len(values) == 1 else ""
    return {
        "text": text,
        "opencv": cv_text,
        "zxing": zx_values,
        "conflict": len(values) > 1,
    }


def n02_decode(pixels):
    _, display_bytes = n02_png(pixels)
    return n02_decode_bytes(display_bytes.tobytes())
