import platform
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

IS_WINDOWS = platform.system() == "Windows"
IS_MAC     = platform.system() == "Darwin"

a = Analysis(
    ["app.py"],
    pathex=["."],
    binaries=[
        *collect_dynamic_libs("llama_cpp"),
    ],
    datas=[
        ("assets", "assets"),
        *collect_data_files("customtkinter"),
        *collect_data_files("llama_cpp"),
    ],
    hiddenimports=[
        "llama_cpp",
        "llama_cpp.llama_cpp",
        "llama_cpp.llama_types",
        "pystray._win32" if IS_WINDOWS else "pystray._darwin",
        "PIL._tkinter_finder",
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

if IS_MAC:
    app = BUNDLE(
        coll,
        name="StudentAI.app",
        icon="assets/logo.png",
        bundle_identifier="au.edu.marsdenparkac.studentai",
    )
