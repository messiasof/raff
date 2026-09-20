"""
Script de geração do instalador MSI com cx_Freeze
"""

import sys
from pathlib import Path
from cx_Freeze import setup, Executable

BASE_DIR = Path(__file__).resolve().parent.parent

build_exe_options = {
    "packages": [
        "os", "sys", "PyQt6", "fastapi", "uvicorn",
        "cryptography", "bcrypt", "win11toast", "google.genai"
    ],
    "include_files": [
        (str(BASE_DIR / "raff" / "gui" / "assets"), "raff/gui/assets"),
    ],
    "excludes": ["tkinter"],
}

bdist_msi_options = {
    "add_to_path": True,
    "initial_target_dir": r"[ProgramFilesFolder]\RAFF",
}

executables = [
    Executable(
        script="raff/gui/tray.py",
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="raff.exe",
        shortcut_name="R.A.F.F",
        shortcut_dir="DesktopFolder",
    )
]

setup(
    name="RAFF",
    version="2.0.0",
    description="Rotina de Aprendizado e Foco Familiar",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
)
