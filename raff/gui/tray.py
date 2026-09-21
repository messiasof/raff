"""
Aplicação de bandeja do sistema (System Tray) do R.A.F.F
Permanece em execução em background, gerencia o agendador e notificações.
"""

import sys
import winreg
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QMessageBox
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal

from raff.core.config import SCHEDULED_TIMES, START_WARNING_MINUTES, ASSETS_DIR
from raff.core.scheduler import get_scheduler
from raff.core.network import enable_network, disable_network
from raff.core.ai_engine import generate_questions, get_fallback_questions
from raff.core.security import is_admin_password_set
from raff.warn import show_warning
from raff.gui.main_window import MainWindow
from raff.gui.quiz_window import QuizWindow
from raff.gui.admin_dialog import prompt_admin_password


RUN_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "RAFF_AutismHelper"


class QuizWorker(QThread):
    """
    Worker thread que executa disable_network + generate_questions fora da
    thread principal do Qt, evitando que a UI trave durante operações lentas.
    Emite 'ready' com a lista de questões quando termina.
    """
    ready = pyqtSignal(list)

    def run(self):
        disable_network()
        try:
            questions = generate_questions()
        except Exception:
            questions = get_fallback_questions()
        self.ready.emit(questions)


def set_autostart(enable: bool, executable_path: str = None) -> bool:
    """Configura inicialização automática com o Windows no registro HKCU."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_REG_KEY, 0, winreg.KEY_SET_VALUE)
        if enable and executable_path:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{executable_path}"')
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


class RaffTrayApp:
    """Controlador da aplicação de bandeja (System Tray)."""

    def __init__(self, app: QApplication):
        self.app = app
        self.main_window = None
        self.quiz_window = None

        icon_path = ASSETS_DIR / "RAFF_Icon.ico"
        if not icon_path.exists():
            icon_path = ASSETS_DIR / "icon.png"
        self.icon = QIcon(str(icon_path)) if icon_path.exists() else app.style().standardIcon(app.style().StandardPixmap.SP_ComputerIcon)

        self.tray_icon = QSystemTrayIcon(self.icon, self.app)
        self.tray_icon.setToolTip("R.A.F.F — Rotina de Aprendizado Focada e Flexível")

        self._create_menu()
        self._setup_scheduler()

        # Clique simples (esquerdo) abre as configurações
        self.tray_icon.activated.connect(self._on_tray_activated)

        self.tray_icon.show()

        # Na primeira execução (sem senha configurada), abre as configurações automaticamente
        if not is_admin_password_set():
            QTimer.singleShot(500, self.open_settings)

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.open_settings()

    def _create_menu(self):
        menu = QMenu()

        action_quiz = QAction("Executar Sessão de Quiz Agora", menu)
        action_quiz.triggered.connect(self.trigger_quiz)
        menu.addAction(action_quiz)

        action_settings = QAction("Abrir Configurações", menu)
        action_settings.triggered.connect(self.open_settings)
        menu.addAction(action_settings)

        menu.addSeparator()

        action_about = QAction("Sobre o R.A.F.F", menu)
        action_about.triggered.connect(self.show_about)
        menu.addAction(action_about)

        menu.addSeparator()

        action_exit = QAction("Sair do R.A.F.F (Responsável)", menu)
        action_exit.triggered.connect(self.exit_app)
        menu.addAction(action_exit)

        self.tray_icon.setContextMenu(menu)

    def _setup_scheduler(self):
        scheduler = get_scheduler()
        scheduler.set_schedules(SCHEDULED_TIMES)
        scheduler.set_warning_lead_time(START_WARNING_MINUTES)
        scheduler.set_callbacks(
            trigger_callback=self.trigger_quiz,
            warning_callback=self._on_warning,
        )
        scheduler.start()

    def _on_warning(self, remaining_minutes: int):
        show_warning(minutes_remaining=remaining_minutes)

    def trigger_quiz(self):
        """Dispara o worker em background; a UI continua responsiva durante o carregamento."""
        # Guarda referência para o worker não ser coletado pelo GC antes de terminar
        self._quiz_worker = QuizWorker()
        self._quiz_worker.ready.connect(self._launch_quiz)
        self._quiz_worker.start()

    def _launch_quiz(self, questions: list):
        """Chamado pela thread principal quando o worker termina — sempre seguro para UI."""
        self.quiz_window = QuizWindow(questions)
        self.quiz_window.show()

    def open_settings(self):
        if not self.main_window:
            self.main_window = MainWindow()
        self.main_window.show()
        self.main_window.activateWindow()
        self.main_window.raise_()

    def show_about(self):
        QMessageBox.information(
            None,
            "Sobre o R.A.F.F",
            "<h3>R.A.F.F v2.0</h3>"
            "<p><b>Rotina de Aprendizado Focada e Flexível</b></p>"
            "<p>Aplicação nativa para apoio cognitivo, rotina de estudos estruturada e acessibilidade.</p>"
            "<p>Desenvolvido com carinho e foco pedagógico.</p>"
        )

    def exit_app(self):
        # Exige senha do responsável para encerrar
        if prompt_admin_password():
            enable_network()
            scheduler = get_scheduler()
            scheduler.stop()
            self.app.quit()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray = RaffTrayApp(app)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
