# PDF Page Duplicator (macOS app + CLI)

This repo includes:

- **CLI tool**: duplicate PDF pages and isolate form fields.
- **Desktop app** (macOS): simple UI for selecting files, page index, copies, and field overrides.

## 1) Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install py2app
```

## 2) Run the app directly

```bash
python pdf_page_duplicator_gui.py
```

## 3) Build a macOS `.app`

```bash
python setup.py py2app
open dist/PDF\ Page\ Duplicator.app
```

## 4) CLI usage

```bash
python pdf_page_duplicator.py \
  --input input.pdf \
  --output output.pdf \
  --source-page 2 \
  --copies 3 \
  --field customer='Jane {copy}' \
  --field invoice='INV-{page}-{copy}'
```

## Notes

- `--source-page` is **0-based**.
- Field override format is `key=value` (one per line in app UI).
- Tokens supported: `{copy}` and `{page}`.
