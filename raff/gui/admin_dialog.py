"""
Diálogo de autenticação e configuração de senha do administrador
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

from raff.core.security import (
    is_admin_password_set,
    setup_admin_password,
    verify_admin_password,
    AVISO_SEM_RECUPERACAO,
)
from raff.gui.styles import THEME_STYLESHEET


class AdminDialog(QDialog):
    """Diálogo modal seguro para solicitar ou cadastrar senha do administrador."""

    def __init__(self, parent=None, title="Autenticação do Responsável"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(440, 280)
        self.setStyleSheet(THEME_STYLESHEET)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self.is_first_setup = not is_admin_password_set()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title_lbl = QLabel("Área do Responsável" if not self.is_first_setup else "Configurar Senha de Acesso")
        title_lbl.setObjectName("titleLabel")
        layout.addWidget(title_lbl)

        if self.is_first_setup:
            info_lbl = QLabel(
                "Crie uma senha para proteger as configurações do R.A.F.F.\n"
                f"<b>{AVISO_SEM_RECUPERACAO}</b>"
            )
            info_lbl.setWordWrap(True)
            info_lbl.setStyleSheet("color: #DC2626; font-size: 12px;")
            layout.addWidget(info_lbl)

            self.pwd_input = QLineEdit()
            self.pwd_input.setPlaceholderText("Digite a nova senha")
            self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addWidget(self.pwd_input)

            self.pwd_confirm = QLineEdit()
            self.pwd_confirm.setPlaceholderText("Confirme a nova senha")
            self.pwd_confirm.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addWidget(self.pwd_confirm)
        else:
            info_lbl = QLabel("Digite a senha do responsável para continuar:")
            layout.addWidget(info_lbl)

            self.pwd_input = QLineEdit()
            self.pwd_input.setPlaceholderText("Senha do responsável")
            self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addWidget(self.pwd_input)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("secondaryButton")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        self.ok_btn = QPushButton("Confirmar" if not self.is_first_setup else "Criar Senha")
        self.ok_btn.clicked.connect(self._handle_submit)
        btn_layout.addWidget(self.ok_btn)

        layout.addLayout(btn_layout)

    def _handle_submit(self):
        pwd = self.pwd_input.text().strip()

        if self.is_first_setup:
            confirm = self.pwd_confirm.text().strip()
            if not pwd:
                QMessageBox.warning(self, "Aviso", "A senha não pode ser vazia.")
                return
            if pwd != confirm:
                QMessageBox.warning(self, "Aviso", "As senhas digitadas não coincidem.")
                return
            setup_admin_password(pwd)
            QMessageBox.information(self, "Sucesso", "Senha do responsável configurada com sucesso!")
            self.accept()
        else:
            if verify_admin_password(pwd):
                self.accept()
            else:
                QMessageBox.critical(self, "Acesso Negado", "Senha incorreta. Tente novamente.")
                self.pwd_input.clear()
                self.pwd_input.setFocus()


def prompt_admin_password(parent=None) -> bool:
    """Função utilitária para abrir o diálogo de senha do admin."""
    dlg = AdminDialog(parent)
    return dlg.exec() == QDialog.DialogCode.Accepted
