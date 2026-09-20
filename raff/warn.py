"""
Módulo de aviso prévio e notificações toast nativas do Windows
Suporta toast notification moderna via win11toast e fallback gracioso.
"""

import sys
import platform
from pathlib import Path
from typing import Optional

from raff.core.config import (
    START_WARNING_ENABLED,
    START_WARNING_TITLE,
    START_WARNING_SOUND,
    ASSETS_DIR,
)


def show_toast(
    title: str,
    message: str,
    duration: str = "short",
    audio: bool = True,
) -> bool:
    """Exibe uma notificação toast nativa no Windows 10/11."""
    if platform.system() != "Windows":
        print(f"[{title}] {message}")
        return True

    try:
        from win11toast import toast
        icon_path = ASSETS_DIR / "icon.png"
        icon = str(icon_path) if icon_path.exists() else None
        
        toast(
            title=title,
            dialogue=message,
            duration=duration,
            icon=icon,
            audio=None if not audio else "ms-winsoundevent:Notification.Default",
        )
        return True
    except Exception:
        # Fallback para ctypes MessageBox em caso de falha no win11toast
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1000)
            return True
        except Exception:
            print(f"[{title}] {message}")
            return False


def show_warning(
    message: Optional[str] = None,
    minutes_remaining: Optional[int] = None,
) -> None:
    """
    Exibe aviso de início iminente da rotina de aprendizado.
    """
    if not START_WARNING_ENABLED:
        return

    if minutes_remaining is not None:
        msg = f"Atenção! Sua sessão de estudos começará em {minutes_remaining} minutos. Salve seu trabalho."
    else:
        msg = message or "Atenção! Sua sessão de estudos começará em instantes."

    show_toast(
        title=START_WARNING_TITLE,
        message=msg,
        audio=START_WARNING_SOUND,
    )


def main():
    if len(sys.argv) > 1:
        custom_msg = " ".join(sys.argv[1:])
        show_toast(START_WARNING_TITLE, custom_msg)
    else:
        show_warning()


if __name__ == "__main__":
    main()
