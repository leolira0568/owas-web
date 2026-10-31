"""Genera OWASWeb.html, un solo archivo que funciona sin internet.

Toma src/OWASWeb.html y reemplaza cada marcador @@MP_...@@ por el archivo
correspondiente de vendor/mediapipe codificado en base64.

Uso: python build.py
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
VENDOR = ROOT / 'vendor' / 'mediapipe'
ASSETS = {
    'MP_BUNDLE': 'vision_bundle.mjs',
    'MP_LOADER': 'vision_wasm_internal.js',
    'MP_WASM': 'vision_wasm_internal.wasm',
    'MP_MODEL': 'pose_landmarker_full.task',
}

html = (ROOT / 'src' / 'OWASWeb.html').read_text(encoding='utf-8')
for key, name in ASSETS.items():
    marker = f'@@{key}@@'
    if html.count(marker) != 1:
        raise SystemExit(f'Se esperaba exactamente un marcador {marker} en src/OWASWeb.html')
    html = html.replace(marker, base64.b64encode((VENDOR / name).read_bytes()).decode('ascii'))

out = ROOT / 'OWASWeb.html'
out.write_text(html, encoding='utf-8', newline='')
print(f'{out.name}: {out.stat().st_size / 1e6:.1f} MB')
