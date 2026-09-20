"""
Janela Principal de Configurações (PyQt6)
Possui abas para o Perfil do Estudante, Área do Responsável (protegida por senha),
Banco Local de Questões e Estatísticas/Diário.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTimeEdit, QComboBox,
    QCheckBox, QMessageBox, QFileDialog, QGroupBox, QSpinBox
)
from PyQt6.QtCore import Qt, QTime

from raff.core.config import (
    STUDENT_NAME, TEACHER_NAME, GEMINI_API_KEY,
    START_WARNING_ENABLED, START_WARNING_MINUTES,
    COMPLETE_SOUND_PATH, NETWORK_DEVICE_1, NETWORK_DEVICE_2,
    API_PORT, SCHEDULED_TIMES
)
from raff.core.storage import (
    load_settings, save_settings, get_feedbacks, get_stats
)
from raff.core.security import (
    is_admin_password_set, setup_admin_password, verify_admin_password
)
from raff.gui.styles import THEME_STYLESHEET
from raff.gui.admin_dialog import prompt_admin_password
from raff.gui.questions_editor import QuestionsEditorWidget


class MainWindow(QMainWindow):
    """Janela principal com interface por abas e proteção de acesso."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("R.A.F.F — Configurações e Acompanhamento")
        self.setMinimumSize(780, 560)
        self.setStyleSheet(THEME_STYLESHEET)

        self.admin_authenticated = False
        self._init_ui()

    def _init_ui(self):
        self.tabs = QTabWidget(self)
        self.tabs.currentChanged.connect(self._on_tab_changed)

        # 1. Aba Estudante (Livre)
        self.student_tab = self._create_student_tab()
        self.tabs.addTab(self.student_tab, "Meu Perfil (Estudante)")

        # 2. Aba Responsável (Protegida)
        self.teacher_tab = self._create_teacher_tab()
        self.tabs.addTab(self.teacher_tab, "Área do Responsável 🔒")

        # 3. Aba Questões (Protegida)
        self.questions_tab = QuestionsEditorWidget()
        self.tabs.addTab(self.questions_tab, "Banco de Questões 🔒")

        # 4. Aba Estatísticas (Livre)
        self.stats_tab = self._create_stats_tab()
        self.tabs.addTab(self.stats_tab, "Estatísticas e Progresso")

        self.setCentralWidget(self.tabs)

    def _on_tab_changed(self, index: int):
        # Abas 1 (Responsável) e 2 (Questões) requerem senha
        if index in (1, 2) and not self.admin_authenticated:
            if prompt_admin_password(self):
                self.admin_authenticated = True
            else:
                self.tabs.setCurrentIndex(0)

    # --- ABA ESTUDANTE ---
    def _create_student_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("Configurações Pessoais do Estudante")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        group = QGroupBox("Perfil")
        g_layout = QVBoxLayout(group)
        g_layout.setSpacing(10)

        g_layout.addWidget(QLabel("Seu Nome ou Apelido:"))
        self.student_name_input = QLineEdit(STUDENT_NAME)
        g_layout.addWidget(self.student_name_input)

        g_layout.addWidget(QLabel("Som de Celebração (.wav):"))
        sound_layout = QHBoxLayout()
        self.sound_input = QLineEdit(COMPLETE_SOUND_PATH)
        sound_layout.addWidget(self.sound_input)

        browse_sound_btn = QPushButton("Escolher Som...")
        browse_sound_btn.setObjectName("secondaryButton")
        browse_sound_btn.clicked.connect(self._browse_sound)
        sound_layout.addWidget(browse_sound_btn)
        g_layout.addLayout(sound_layout)

        layout.addWidget(group)
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        save_btn = QPushButton("Salvar Meu Perfil")
        save_btn.setObjectName("successButton")
        save_btn.clicked.connect(self._save_student_profile)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        return widget

    def _browse_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo de Som", "", "Áudio (*.wav *.mp3)"
        )
        if file_path:
            self.sound_input.setText(file_path)

    def _save_student_profile(self):
        settings = load_settings()
        settings["STUDENT_NAME"] = self.student_name_input.text().strip()
        settings["COMPLETE_SOUND_PATH"] = self.sound_input.text().strip()
        save_settings(settings)
        QMessageBox.information(self, "Sucesso", "Perfil atualizado com sucesso!")

    # --- ABA RESPONSÁVEL ---
    def _create_teacher_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("Controle Pedagógico e Segurança")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        # Chave de IA e Avisos
        ia_group = QGroupBox("Inteligência Artificial & Rotina")
        ia_layout = QVBoxLayout(ia_group)
        ia_layout.addWidget(QLabel("Chave de API Gemini (Opcional):"))
        self.gemini_input = QLineEdit(GEMINI_API_KEY)
        self.gemini_input.setEchoMode(QLineEdit.EchoMode.Password)
        ia_layout.addWidget(self.gemini_input)

        self.warn_check = QCheckBox("Habilitar Notificações de Aviso Prévio")
        self.warn_check.setChecked(START_WARNING_ENABLED)
        ia_layout.addWidget(self.warn_check)

        warn_layout = QHBoxLayout()
        warn_layout.addWidget(QLabel("Minutos de antecedência do aviso:"))
        self.warn_min_spin = QSpinBox()
        self.warn_min_spin.setRange(1, 60)
        self.warn_min_spin.setValue(START_WARNING_MINUTES)
        warn_layout.addWidget(self.warn_min_spin)
        warn_layout.addStretch()
        ia_layout.addLayout(warn_layout)

        layout.addWidget(ia_group)

        # Adaptadores de Rede
        net_group = QGroupBox("Controle de Adaptadores de Rede")
        net_layout = QVBoxLayout(net_group)
        net_layout.addWidget(QLabel("Nome do Adaptador Wi-Fi principal:"))
        self.net1_input = QLineEdit(NETWORK_DEVICE_1)
        net_layout.addWidget(self.net1_input)

        net_layout.addWidget(QLabel("Nome do Adaptador Ethernet/Secundário:"))
        self.net2_input = QLineEdit(NETWORK_DEVICE_2)
        net_layout.addWidget(self.net2_input)
        layout.addWidget(net_group)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        save_teacher_btn = QPushButton("Salvar Configurações do Responsável")
        save_teacher_btn.setObjectName("successButton")
        save_teacher_btn.clicked.connect(self._save_teacher_settings)
        btn_layout.addWidget(save_teacher_btn)
        layout.addLayout(btn_layout)

        return widget

    def _save_teacher_settings(self):
        settings = load_settings()
        settings["GEMINI_API_KEY"] = self.gemini_input.text().strip()
        settings["START_WARNING_ENABLED"] = self.warn_check.isChecked()
        settings["START_WARNING_MINUTES"] = self.warn_min_spin.value()
        settings["NETWORK_DEVICE_1"] = self.net1_input.text().strip()
        settings["NETWORK_DEVICE_2"] = self.net2_input.text().strip()
        save_settings(settings)
        QMessageBox.information(self, "Sucesso", "Configurações pedagógicas salvas com sucesso!")

    # --- ABA ESTATÍSTICAS ---
    def _create_stats_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel("Histórico de Foco e Desempenho")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        stats = get_stats()
        if not stats:
            info = QLabel("Nenhuma sessão de quiz foi registrada ainda.\nConclua a primeira sessão para ver seu progresso!")
            info.setStyleSheet("color: #6C757D; font-size: 14px; margin-top: 20px;")
            layout.addWidget(info)
        else:
            total_quizzes = sum(v.get("total_quiz", 0) for v in stats.values())
            total_acertos = sum(v.get("acertos", 0) for v in stats.values())
            total_perguntas = sum(v.get("total_perguntas", 0) for v in stats.values())
            pct = int((total_acertos / max(1, total_perguntas)) * 100)

            summary_lbl = QLabel(
                f"<b>Sessões Concluídas:</b> {total_quizzes}<br>"
                f"<b>Total de Perguntas Respondidas:</b> {total_perguntas}<br>"
                f"<b>Taxa Geral de Acerto:</b> {pct}%"
            )
            summary_lbl.setStyleSheet("font-size: 15px; background-color: #FFFFFF; padding: 15px; border-radius: 8px; border: 1px solid #E5E7EB;")
            layout.addWidget(summary_lbl)

        layout.addStretch()
        return widget
