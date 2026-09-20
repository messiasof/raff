"""
Script de geração de pacote portátil (.zip) com PyInstaller
"""

import os
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "dist"
BUILD_DIR = BASE_DIR / "build"


def build_portable():
    print("📦 Construindo versão portátil do R.A.F.F...")

    cmd = [
        "pyinstaller",
        "--name=RAFF-Portavel",
        "--windowed",
        "--noconfirm",
        "--add-data=raff/gui/assets;raff/gui/assets",
        "raff/gui/tray.py",
    ]

    subprocess.run(cmd, cwd=BASE_DIR, check=True)
    print("✅ Build portátil concluído em dist/RAFF-Portavel")


if __name__ == "__main__":
    build_portable()
