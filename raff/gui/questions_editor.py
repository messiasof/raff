"""
Editor de questões do banco local protegido por senha
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QLineEdit, QTextEdit,
    QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt

from raff.core.storage import (
    get_local_questions,
    add_local_question,
    delete_local_question,
    save_local_questions,
)
from raff.gui.styles import THEME_STYLESHEET


class QuestionEditDialog(QDialog):
    """Diálogo para adicionar ou editar uma pergunta."""

    def __init__(self, parent=None, question=None):
        super().__init__(parent)
        self.setWindowTitle("Nova Pergunta" if not question else "Editar Pergunta")
        self.setFixedSize(500, 520)
        self.setStyleSheet(THEME_STYLESHEET)
        self.question = question
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Enunciado da Pergunta:"))
        self.pergunta_txt = QTextEdit()
        self.pergunta_txt.setMaximumHeight(80)
        layout.addWidget(self.pergunta_txt)

        layout.addWidget(QLabel("Matéria:"))
        self.materia_input = QLineEdit()
        self.materia_input.setPlaceholderText("Ex: Matemática, Português, Ciências")
        layout.addWidget(self.materia_input)

        layout.addWidget(QLabel("Opções de Resposta:"))
        self.opcoes_inputs = []
        for i in range(4):
            inp = QLineEdit()
            inp.setPlaceholderText(f"Opção {chr(65 + i)}")
            layout.addWidget(inp)
            self.opcoes_inputs.append(inp)

        layout.addWidget(QLabel("Resposta Correta:"))
        self.correta_combo = QComboBox()
        self.correta_combo.addItems(["Opção A", "Opção B", "Opção C", "Opção D"])
        layout.addWidget(self.correta_combo)

        layout.addWidget(QLabel("Explicação Pedagógica:"))
        self.explicacao_txt = QLineEdit()
        self.explicacao_txt.setPlaceholderText("Breve explicação ao acertar/errar")
        layout.addWidget(self.explicacao_txt)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Salvar Pergunta")
        save_btn.setObjectName("successButton")
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        if self.question:
            self.pergunta_txt.setPlainText(self.question.get("pergunta", ""))
            self.materia_input.setText(self.question.get("materia", ""))
            opcoes = self.question.get("opcoes", [])
            for i in range(min(4, len(opcoes))):
                self.opcoes_inputs[i].setText(opcoes[i])
            self.correta_combo.setCurrentIndex(self.question.get("resposta_correta", 0))
            self.explicacao_txt.setText(self.question.get("explicacao", ""))

    def _save(self):
        pergunta = self.pergunta_txt.toPlainText().strip()
        materia = self.materia_input.text().strip() or "Geral"
        opcoes = [inp.text().strip() for inp in self.opcoes_inputs]

        if not pergunta:
            QMessageBox.warning(self, "Aviso", "O enunciado não pode ser vazio.")
            return
        if any(not op for op in opcoes):
            QMessageBox.warning(self, "Aviso", "Preencha todas as 4 opções de resposta.")
            return

        self.result_data = {
            "pergunta": pergunta,
            "materia": materia,
            "opcoes": opcoes,
            "resposta_correta": self.correta_combo.currentIndex(),
            "explicacao": self.explicacao_txt.text().strip(),
        }
        self.accept()


class QuestionsEditorWidget(QWidget):
    """Widget de gerenciamento e listagem de questões locais."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.load_questions()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        lbl = QLabel("Banco Local de Questões (Offline)")
        lbl.setObjectName("titleLabel")
        header_layout.addWidget(lbl)
        header_layout.addStretch()

        add_btn = QPushButton("+ Nova Questão")
        add_btn.setObjectName("successButton")
        add_btn.clicked.connect(self._add_question)
        header_layout.addWidget(add_btn)
        layout.addLayout(header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Matéria", "Pergunta", "Opção Correta"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        del_btn = QPushButton("Excluir Selecionada")
        del_btn.setObjectName("dangerButton")
        del_btn.clicked.connect(self._delete_selected)
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)

    def load_questions(self):
        questions = get_local_questions()
        self.table.setRowCount(len(questions))
        for row, q in enumerate(questions):
            self.table.setItem(row, 0, QTableWidgetItem(str(q.get("id", row + 1))))
            self.table.setItem(row, 1, QTableWidgetItem(q.get("materia", "Geral")))
            self.table.setItem(row, 2, QTableWidgetItem(q.get("pergunta", "")))
            correta_idx = q.get("resposta_correta", 0)
            opcoes = q.get("opcoes", [])
            correta_txt = opcoes[correta_idx] if correta_idx < len(opcoes) else ""
            self.table.setItem(row, 3, QTableWidgetItem(correta_txt))

    def _add_question(self):
        dlg = QuestionEditDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            add_local_question(dlg.result_data)
            self.load_questions()

    def _delete_selected(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.information(self, "Aviso", "Selecione uma questão na tabela para excluir.")
            return

        id_item = self.table.item(selected_row, 0)
        if not id_item:
            return

        q_id = int(id_item.text())
        if QMessageBox.question(
            self, "Confirmação", "Tem certeza que deseja excluir esta questão?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            delete_local_question(q_id)
            self.load_questions()
