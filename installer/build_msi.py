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
_versao_raw = re.sub(r"(?i)^v", "", _ler_versao()) or "0"

# Converte versões com sufixo de letra (ex: "2b", "3a") para PEP 440 válido.
# "2b" → version="2.0.0b0"  (usado no setup())
# "2b" → _versao_num="2"    (usado no nome do artefato, que já vem do .raffver)
_letter_match = re.match(r"^(\d+)([a-z]+)(\d*)$", _versao_raw, re.IGNORECASE)
if _letter_match:
    _versao_num = _letter_match.group(1)          # parte numérica pura  → "2"
    _versao_pep440 = (
        f"{_letter_match.group(1)}.0.0"
        f"{_letter_match.group(2).lower()}"
        f"{_letter_match.group(3) or '0'}"        # "2b" → "2.0.0b0"
    )
else:
    _versao_num = _versao_raw
    _versao_pep440 = f"{_versao_raw}.0.0"

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
    "install_icon": str(BASE_DIR / "raff" / "gui" / "assets" / "RAFF_Icon.ico")
    if (BASE_DIR / "raff" / "gui" / "assets" / "RAFF_Icon.ico").exists()
    else None,
}

_ico = BASE_DIR / "raff" / "gui" / "assets" / "RAFF_Icon.ico"

executables = [
    Executable(
        script=str(BASE_DIR / "raff" / "gui" / "tray.py"),
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="raff.exe",
        icon=str(_ico) if _ico.exists() else None,
        shortcut_name="R.A.F.F",
        shortcut_dir="DesktopFolder",
    )
]

setup(
    name=_nome,
    version=_versao_pep440,
    description="Rotina de Aprendizado Focada e Flexível",
    author="Emanuel Messias",
    author_email="contato@messias.me",
    url="https://messias.me",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
)
