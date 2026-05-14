# Student AI Support

A lightweight, local AI tool for students. Highlight any text, press **Ctrl+Shift+A**, and choose:
- **Explain this** — plain-language explanation
- **Summarise this** — bullet-point summary
- **Test me on this** — 3 multiple-choice questions

Runs fully offline after first setup. No accounts, no cloud, no data leaves the machine.

---

## Setup (Development)

### 1. Prerequisites
- Python 3.11 or 3.12
- Windows 10/11

### 2. Install dependencies
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download the llamafile binary
```
python download_llamafile.py
```

### 4. Run
```
python app.py
```

On first launch, the app will download the default AI model (~1.9 GB). This is a one-time step.

After that, a tray icon appears. Highlight text anywhere and press **Ctrl+Shift+A**.

---

## Models

| Model | Size | Best for |
|---|---|---|
| Qwen2.5 3B (default) | ~1.9 GB | All subjects |
| Qwen2.5 Coder 3B | ~1.9 GB | CS / IT classes |
| Qwen2.5 7B | ~4.5 GB | Stronger laptops |

Additional models can be downloaded from **Settings** (right-click the tray icon).
