"""
Módulo de aviso prévio desacoplado
Pode ser executado independentemente para mostrar avisos customizados
Uso: python -m src.warn "Sua mensagem aqui"
Ou via CLI: raff warn "Sua mensagem aqui"
"""

import sys
import argparse
import ctypes
import platform
from pathlib import Path

from src.config import START_WARNING_ENABLED, START_WARNING_TITLE


def show_warning(message: str) -> None:
    """
    Mostra um aviso nativo do Windows com a mensagem fornecida.
    
    Args:
        message: Mensagem a exibir no aviso
    """
    if not START_WARNING_ENABLED:
        print(message)
        return

    if platform.system() != "Windows":
        print(message)
        return

    try:
        message_box = ctypes.windll.user32.MessageBoxW
        message_box(
            0,
            message,
            START_WARNING_TITLE,
            0x40,  # MB_ICONINFORMATION
        )
    except Exception:
        print(message)


def main():
    """Ponto de entrada para o módulo warn."""
    parser = argparse.ArgumentParser(
        prog="warn",
        description="Exibe um aviso nativo do Windows com mensagem customizada",
    )
    parser.add_argument(
        "message",
        nargs="?",
        default="Aviso do R.A.F.F",
        help="Mensagem a exibir no aviso",
    )

    args = parser.parse_args()
    show_warning(args.message)


if __name__ == "__main__":
    main()
