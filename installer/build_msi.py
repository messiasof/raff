"""
Script de geração do instalador MSI com cx_Freeze.
O nome do artefato é lido da variável de ambiente RAFF_NOME_INSTALADOR,
ou derivado diretamente do .raffver na raiz do projeto.
"""

import os
import re
import sys
from pathlib import Path

from cx_Freeze import setup, Executable


BASE_DIR = Path(__file__).resolve().parent.parent


def _ler_versao() -> str:
    """Lê a versão do .raffver e devolve no formato 'V2'."""
    raffver = BASE_DIR / ".raffver"
    if not raffver.exists():
        return "V0"
    for linha in raffver.read_text(encoding="utf-8").splitlines():
        if linha.upper().startswith("VERSION"):
            _, _, valor = linha.partition("=")
            valor = valor.strip().strip('"').strip("'")
            valor = re.sub(r"(?i)^v", "", valor)
            return f"V{valor}" if valor else "V0"
    return "V0"


def _nome_instalador() -> str:
    """Devolve o nome do artefato instalador."""
    return os.environ.get("RAFF_NOME_INSTALADOR") or f"RAFF_{_ler_versao()}-Instalador"


_nome = _nome_instalador()
_versao_num = re.sub(r"(?i)^v", "", _ler_versao()) or "0"

build_exe_options = {
    "packages": [
        "os", "sys", "PyQt6", "fastapi", "uvicorn",
        "cryptography", "bcrypt", "win11toast", "google.genai",
    ],
    "include_files": [
        (str(BASE_DIR / "raff" / "gui" / "assets"), "raff/gui/assets"),
    ],
    "excludes": ["tkinter"],
    "build_exe": str(BASE_DIR / "dist" / _nome),
}

bdist_msi_options = {
    "add_to_path": True,
    "initial_target_dir": r"[ProgramFilesFolder]\RAFF",
    "install_icon": str(BASE_DIR / "raff" / "gui" / "assets" / "icon.ico")
    if (BASE_DIR / "raff" / "gui" / "assets" / "icon.ico").exists()
    else None,
}

executables = [
    Executable(
        script=str(BASE_DIR / "raff" / "gui" / "tray.py"),
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="raff.exe",
        shortcut_name="R.A.F.F",
        shortcut_dir="DesktopFolder",
    )
]

setup(
    name=_nome,
    version=f"{_versao_num}.0.0",
    description="Rotina de Aprendizado e Foco Familiar",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
)
