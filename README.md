# Student AI Support — Marsden Park Anglican College

A private, local AI study tool. Highlight any text on your screen, press a keyboard shortcut, and get instant help — no internet required after setup, no accounts, and nothing leaves your device.

---

## What it does

Press **Ctrl+Shift+`** after highlighting any text — in a document, a webpage, a PDF, anything — and choose:

| Option | What you get |
|---|---|
| **Explain this** | A plain-English explanation of the selected text |
| **Summarise this** | Key points as bullet points |
| **Test me on this** | 3 multiple-choice questions with answer checking |

> **Note:** The first response after launching takes a moment while the AI warms up. After that it's faster.
>
> **Tip:** You can change the keyboard shortcut in Settings if it clashes with another app.

---

## For Windows Students

### Step 1 — Download the app
Go to the [Releases page](../../releases) and download **StudentAI-Windows.zip**

### Step 2 — Unzip it
Right-click the zip file → **Extract All** → choose a location (e.g. your Desktop or Documents)

### Step 3 — Run it
Open the `StudentAI` folder and double-click **StudentAI.exe**

> **Windows security warning:** If you see *"Windows protected your PC"*, click **More info** → **Run anyway**. This appears because the app isn't signed with a paid certificate — it's safe.

### Step 4 — Download the AI model (first time only)
A setup window will appear showing where the model will be saved. You can change this location if you like, then click **Start Download** (~1.9 GB). It only happens once.

> **If the download is blocked** (e.g. on school Wi-Fi), see [Manual model download](#manual-model-download) below.

> **Default model location (Windows):** `%LOCALAPPDATA%\StudentAI\models\`
> This folder is *not* synced by OneDrive, so it won't chew up your cloud storage.

### Step 5 — You're ready
A small icon appears in your system tray (bottom-right, near the clock). The app is running in the background.

**To use it:** Highlight any text → press **Ctrl+Shift+`** → choose an option.

**To quit:** Right-click the tray icon → **Quit**

---

## For Mac Students

### Step 1 — Download the app
Go to the [Releases page](../../releases) and download **StudentAI-macOS.zip**

### Step 2 — Unzip it
Double-click the zip file — it will extract **StudentAI.app**

### Step 3 — Open it (important — read carefully)
Because the app isn't signed with a paid Apple certificate, macOS will block it the first time.

**Do this once:**
1. **Right-click** StudentAI.app (or two-finger tap on trackpad)
2. Click **Open**
3. Click **Open** again in the warning dialog

After this, it will open normally every time.

### Step 4 — Allow keyboard access (first time only)
The app needs permission to detect your keyboard shortcut from any app.

When the permission prompt appears:
1. Click **Open System Settings**
2. Find **Student AI Support** in the list
3. Toggle it **on**
4. Switch back to the app

### Step 5 — Download the AI model (first time only)
A setup window will appear showing where the model will be saved. You can change this location if you like, then click **Start Download** (~1.9 GB). It only happens once.

> **If the download is blocked** (e.g. on school Wi-Fi), see [Manual model download](#manual-model-download) below.

> **Default model location (Mac):** `~/Library/Application Support/StudentAI/models/`
> This folder is not synced by iCloud Drive.

### Step 6 — You're ready
A small icon appears in your menu bar (top-right). The app is running in the background.

**To use it:** Highlight any text → press **Ctrl+Shift+`** → choose an option.

**To quit:** Click the menu bar icon → **Quit**

---

## Manual model download

If the automatic download is blocked by your school network, you can download the model file at home and copy it across.

### Step 1 — Download the model file
**[Download Qwen2.5-3B-Instruct-Q4_K_M.gguf](https://huggingface.co/bartowski/Qwen2.5-3B-Instruct-GGUF/resolve/main/Qwen2.5-3B-Instruct-Q4_K_M.gguf)** (~1.9 GB)

page link: [Bartowski Qwen2.5-3B-Q4_K_M](https://huggingface.co/bartowski/Qwen2.5-3B-Instruct-GGUF/blob/main/Qwen2.5-3B-Instruct-Q4_K_M.gguf)

This is the AI "brain" the app uses. Download it on a home connection (or any network that allows it).

### Step 2 — Place it in the models folder

**Windows:**
1. Open File Explorer and go to: `%LOCALAPPDATA%\StudentAI\models\`
   *(Type that path directly into the address bar — Windows will expand it)*
2. If the `models` folder doesn't exist yet, create it
3. Copy the downloaded `.gguf` file into that folder

**Mac:**
1. Open Finder and go to: `~/Library/Application Support/StudentAI/models/`
   *(In Finder: Go menu → Go to Folder… → paste the path)*
2. If the `models` folder doesn't exist yet, create it
3. Copy the downloaded `.gguf` file into that folder

> **Tip:** You can also choose a different folder entirely. On first launch, the setup screen lets you change the models location — point it at whatever folder you put the file in.

### Step 3 — Launch the app
Double-click `StudentAI.exe` (Windows) or `StudentAI.app` (Mac). The setup screen will appear — if the model file is already in the folder, it will show **"✓ Model found — no download needed"** and you can click Continue.

---

## Getting help

Right-click the tray icon (Windows) or menu bar icon (Mac) → **Help** to open this page.
You can also find it in **Settings → Help** (top-right of the Settings window).

---

## Troubleshooting

**Nothing happens when I press the shortcut**
- Check the tray/menu bar icon is still running — if not, relaunch the app
- Make sure you actually highlighted (selected) some text before pressing the shortcut
- If another app uses the same shortcut, change it in Settings (right-click tray icon → Settings)

**"No text selected" message**
- The shortcut was pressed without highlighted text. Select some text first, then press the shortcut
- In Adobe Reader / PDF viewers: select your text, press **Ctrl+C** first, then press the shortcut

**The response is slow**
- This is normal, especially on Windows. The AI runs entirely on your device with no internet. Mac users on Apple Silicon (M1/M2/M3) will generally see faster responses.

**Mac: the app won't open at all**
- Make sure you used right-click → Open (not double-click) the very first time

**Windows: the app crashes on startup**
- Check that the `models` folder inside your StudentAI folder contains a `.gguf` file. If it's empty, re-run the app to trigger the download, or follow the manual download steps above.

---

## For Teachers — Building and Releasing

### How releases work
This repo uses GitHub Actions to automatically build both the Windows and Mac versions whenever you create a new release tag. You don't need a Mac to produce the Mac build.

### Creating a new release

1. Make your code changes and commit them as normal
2. Tag the release:
```
git tag v1.1
git push origin v1.1
```
3. GitHub Actions will automatically:
   - Build `StudentAI-Windows.zip` on a Windows machine
   - Build `StudentAI-macOS.zip` on a Mac machine
   - Attach both files to a new Release on GitHub

4. Go to the [Releases page](../../releases) — both downloads will be there within ~5 minutes

### Sharing with students
Send students the link to the Releases page, or copy the direct download links for each file. The model download happens on the student's machine on first launch — you don't need to distribute it.

If your school network blocks HuggingFace, share the [manual model download link](#manual-model-download) with students and ask them to do it at home.

### Updating students to a new version
Students can check for updates via **Settings → Advanced → Check for updates**, or by right-clicking the tray icon → **Check for updates**.

To install an update, students just download the new zip and extract it **over the top of their existing StudentAI folder**. Their settings and AI models are stored separately and will be kept automatically — no need to re-download the model.

### Development setup (if you want to run from source)
Requires Python 3.11 or 3.12.

```
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py

# macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Switching or adding AI models
Right-click the tray icon → **Settings** → download additional models or switch the active one. Available models:

| Model | Size | Best for |
|---|---|---|
| Qwen2.5 3B (default) | ~1.9 GB | All subjects |
| Qwen2.5 Coder 3B | ~1.9 GB | Computing / IT classes |
| Qwen2.5 7B | ~4.5 GB | Stronger machines only |

> **Advanced:** Any GGUF-format model file placed in the `models` folder will appear in the Settings dropdown automatically.
