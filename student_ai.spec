import sys
import platform
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

IS_WINDOWS = platform.system() == "Windows"
IS_MAC     = platform.system() == "Darwin"

llamafile_bin = ("bin/llamafile.exe", "bin") if IS_WINDOWS else ("bin/llamafile", "bin")

a = Analysis(
    ["app.py"],
    pathex=["."],
    binaries=[llamafile_bin],
    datas=[
        ("assets", "assets"),
        *collect_data_files("customtkinter"),
    ],
    hiddenimports=[
        "pystray._win32"   if IS_WINDOWS else "pystray._darwin",
        "PIL._tkinter_finder",
        "customtkinter",
    ],
    hookspath=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="StudentAI",
    icon="assets/logo.png",
    console=False,
    windowed=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="StudentAI",
)

# macOS: also wrap in a .app bundle
if IS_MAC:
    app = BUNDLE(
        coll,
        name="StudentAI.app",
        icon="assets/logo.png",
        bundle_identifier="au.edu.marsdenparkac.studentai",
    )
