"""
Script de geração de pacote portátil (.zip) com PyInstaller.
O nome do artefato é lido da variável de ambiente RAFF_NOME_PORTAVEL,
ou derivado diretamente do .raffver na raiz do projeto.
"""

import os
import re
import subprocess
import shutil
from pathlib import Path


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


def _nome_portavel() -> str:
    """Devolve o nome do artefato portátil."""
    return os.environ.get("RAFF_NOME_PORTAVEL") or f"RAFF_{_ler_versao()}-Portatil"


def build_portable():
    nome = _nome_portavel()
    print(f"Construindo versão portátil do R.A.F.F como '{nome}'...")

    cmd = [
        "pyinstaller",
        f"--name={nome}",
        "--windowed",
        "--noconfirm",
        "--add-data=raff/gui/assets;raff/gui/assets",
        "raff/gui/tray.py",
    ]

    subprocess.run(cmd, cwd=BASE_DIR, check=True)

    pasta = BASE_DIR / "dist" / nome
    if pasta.exists():
        zip_destino = BASE_DIR / "dist" / f"{nome}.zip"
        shutil.make_archive(str(BASE_DIR / "dist" / nome), "zip", str(pasta))
        print(f"Portátil gerado em: {zip_destino}")
    else:
        print(f"Concluído em dist/{nome}")


if __name__ == "__main__":
    build_portable()
