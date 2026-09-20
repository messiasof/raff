"""
Janela gráfica do Quiz (PyQt6)
Substitui a interface em terminal urwid, com foco cognitivo, acessibilidade e sons de conclusão.
"""

import sys
import time
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup,
    QProgressBar, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from raff.core.config import COMPLETE_SOUND_PATH, STUDENT_NAME
from raff.core.storage import record_quiz_result
from raff.core.network import enable_network
from raff.gui.styles import THEME_STYLESHEET


def _play_success_sound():
    """Reproduz som de sucesso de forma segura no Windows."""
    if not COMPLETE_SOUND_PATH:
        return
    try:
        import winsound
        winsound.PlaySound(COMPLETE_SOUND_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception:
        pass


class QuizWindow(QWidget):
    """Janela do Quiz interativo em PyQt6."""

    def __init__(self, questions: List[Dict], parent=None):
        super().__init__(parent)
        self.questions = questions
        self.current_idx = 0
        self.score = 0
        self.start_time = time.time()

        self.setWindowTitle(f"R.A.F.F — Sessão de Aprendizado de {STUDENT_NAME}")
        self.setMinimumSize(700, 520)
        self.setStyleSheet(THEME_STYLESHEET)
        
        # Bloqueia botão de fechar durante o quiz
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)

        self._init_ui()
        self._load_current_question()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(16)

        # Header: Progresso e Matéria
        header_layout = QHBoxLayout()
        self.subject_lbl = QLabel("Matéria: Geral")
        self.subject_lbl.setStyleSheet("font-weight: bold; color: #1E3A8A; font-size: 16px;")
        header_layout.addWidget(self.subject_lbl)
        header_layout.addStretch()

        self.progress_lbl = QLabel("Pergunta 1 de 5")
        self.progress_lbl.setStyleSheet("color: #6C757D; font-size: 14px;")
        header_layout.addWidget(self.progress_lbl)
        main_layout.addLayout(header_layout)

        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.questions))
        self.progress_bar.setValue(1)
        main_layout.addWidget(self.progress_bar)

        # Card da Questão
        self.card_frame = QFrame()
        self.card_frame.setStyleSheet("background-color: #FFFFFF; border: 2px solid #E5E7EB; border-radius: 10px; padding: 15px;")
        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setSpacing(14)

        self.question_lbl = QLabel("")
        self.question_lbl.setWordWrap(True)
        self.question_lbl.setStyleSheet("font-size: 17px; font-weight: bold; color: #1F2937;")
        card_layout.addWidget(self.question_lbl)

        # Grupo de Opções (Radio Buttons)
        self.button_group = QButtonGroup(self)
        self.option_radios: List[QRadioButton] = []
        for i in range(4):
            radio = QRadioButton("")
            radio.setStyleSheet("font-size: 15px; padding: 6px; color: #374151;")
            self.button_group.addButton(radio, i)
            card_layout.addWidget(radio)
            self.option_radios.append(radio)

        main_layout.addWidget(self.card_frame)

        # Feedback/Explicação inline
        self.feedback_lbl = QLabel("")
        self.feedback_lbl.setWordWrap(True)
        self.feedback_lbl.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.feedback_lbl.hide()
        main_layout.addWidget(self.feedback_lbl)

        # Botão de Ação
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.action_btn = QPushButton("Confirmar Resposta")
        self.action_btn.setMinimumWidth(180)
        self.action_btn.clicked.connect(self._handle_action)
        btn_layout.addWidget(self.action_btn)

        main_layout.addLayout(btn_layout)
        self.waiting_next = False

    def _load_current_question(self):
        if self.current_idx >= len(self.questions):
            self._finish_quiz()
            return

        q = self.questions[self.current_idx]
        total = len(self.questions)
        self.progress_lbl.setText(f"Pergunta {self.current_idx + 1} de {total}")
        self.progress_bar.setValue(self.current_idx + 1)
        self.subject_lbl.setText(f"Matéria: {q.get('materia', 'Geral')}")
        self.question_lbl.setText(q.get("pergunta", ""))

        opcoes = q.get("opcoes", [])
        self.button_group.setExclusive(False)
        for i, radio in enumerate(self.option_radios):
            if i < len(opcoes):
                radio.setText(opcoes[i])
                radio.setChecked(False)
                radio.setEnabled(True)
                radio.show()
            else:
                radio.hide()
        self.button_group.setExclusive(True)

        self.feedback_lbl.hide()
        self.action_btn.setText("Confirmar Resposta")
        self.action_btn.setObjectName("")
        self.action_btn.setStyleSheet("")
        self.waiting_next = False

    def _handle_action(self):
        if self.waiting_next:
            self.current_idx += 1
            self._load_current_question()
            return

        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            QMessageBox.warning(self, "Aviso", "Selecione uma opção antes de confirmar.")
            return

        q = self.questions[self.current_idx]
        correta = q.get("resposta_correta", 0)
        explicacao = q.get("explicacao", "")

        for r in self.option_radios:
            r.setEnabled(False)

        if selected_id == correta:
            self.score += 1
            self.feedback_lbl.setText(f"✨ Correto! {explicacao}")
            self.feedback_lbl.setStyleSheet("color: #059669; background-color: #ECFDF5; border-radius: 6px; padding: 10px;")
        else:
            self.feedback_lbl.setText(f"❌ Não foi dessa vez. {explicacao}")
            self.feedback_lbl.setStyleSheet("color: #DC2626; background-color: #FEF2F2; border-radius: 6px; padding: 10px;")

        self.feedback_lbl.show()
        self.action_btn.setText("Próxima Pergunta" if self.current_idx + 1 < len(self.questions) else "Ver Resultado")
        self.waiting_next = True

    def _finish_quiz(self):
        elapsed = int(time.time() - self.start_time)
        total = len(self.questions)
        record_quiz_result(self.score, total, elapsed)
        _play_success_sound()
        enable_network()

        # Janela de Conclusão Amigável
        QMessageBox.information(
            self,
            "Parabéns!",
            f"🎉 Sessão concluída com sucesso, {STUDENT_NAME}!\n\n"
            f"Acertos: {self.score} de {total}\n"
            f"Tempo: {elapsed} segundos\n\n"
            "A internet foi liberada. Bom descanso e ótimo foco!"
        )
        self.close()
