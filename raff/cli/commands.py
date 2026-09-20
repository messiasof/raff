"""
Interface de linha de comando do R.A.F.F
Todos os comandos disponíveis via terminal.
"""

import argparse
import sys


def cmd_start(args):
    """Inicia o R.A.F.F. Por padrão abre a interface gráfica (tray). Com --headless usa o terminal."""
    if args.headless:
        from raff.core.main import main as headless_main
        headless_main()
    else:
        cmd_gui(args)


def cmd_gui(args):
    """Inicia o aplicativo com interface gráfica e ícone na bandeja do sistema."""
    from PyQt6.QtWidgets import QApplication
    from raff.gui.tray import RaffTrayApp
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray = RaffTrayApp(app)
    sys.exit(app.exec())


def cmd_warn(args):
    """Exibe uma notificação de aviso."""
    from raff.warn import show_toast
    from raff.core.config import START_WARNING_TITLE
    msg = args.message or "Atenção! Sua sessão de estudos está prestes a começar."
    show_toast(START_WARNING_TITLE, msg)


def cmd_api(args):
    """Inicia o servidor da API REST para controle remoto."""
    from raff.api.server import run_server
    run_server()


def cmd_config(args):
    """Abre a janela de configurações."""
    from PyQt6.QtWidgets import QApplication
    from raff.gui.main_window import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


def cmd_healthcheck(args):
    """Valida a instalação e configuração do R.A.F.F."""
    try:
        import healthcheck
        healthcheck.run_checks()
    except Exception:
        from raff.core import config, storage, security, scheduler, network, ai_engine
        print("Verificação básica concluída. Todos os módulos acessíveis.")


def mainCLI():
    parser = argparse.ArgumentParser(
        prog="raff",
        description="R.A.F.F — Rotina de Aprendizado e Foco Familiar",
    )
    parser.add_argument(
        "--version", action="version", version="R.A.F.F v2.0.0"
    )

    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")

    # raff start [--headless]
    p_start = subparsers.add_parser("start", help="Inicia o R.A.F.F (GUI por padrão)")
    p_start.add_argument(
        "--headless",
        action="store_true",
        help="Inicia em modo terminal sem interface gráfica (retrocompatibilidade)",
    )
    p_start.set_defaults(func=cmd_start)

    # raff gui
    p_gui = subparsers.add_parser("gui", help="Inicia a interface gráfica e bandeja do sistema")
    p_gui.set_defaults(func=cmd_gui)

    # raff warn [mensagem]
    p_warn = subparsers.add_parser("warn", help="Exibe uma notificação de aviso")
    p_warn.add_argument("message", nargs="?", default=None, help="Mensagem personalizada do aviso")
    p_warn.set_defaults(func=cmd_warn)

    # raff api
    p_api = subparsers.add_parser("api", help="Inicia o servidor da API REST")
    p_api.set_defaults(func=cmd_api)

    # raff config
    p_config = subparsers.add_parser("config", help="Abre a janela de configurações")
    p_config.set_defaults(func=cmd_config)

    # raff healthcheck
    p_health = subparsers.add_parser("healthcheck", help="Verifica a instalação e configuração")
    p_health.set_defaults(func=cmd_healthcheck)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        # Comportamento padrão sem subcomando: inicia a GUI
        cmd_gui(args)


if __name__ == "__main__":
    mainCLI()
