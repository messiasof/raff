"""
Módulo de interface do usuário
Interface CLI com urwid para apresentação das perguntas
"""

import urwid # pyright: ignore[reportMissingImports]
from typing import List, Dict, Callable


class QuizUI:
    """Interface de quiz com urwid."""
    
    def __init__(self, questions: List[Dict], on_complete: Callable):
        """
        Inicializa a interface do quiz.
        
        Args:
            questions: Lista de dicionários com 'question', 'explain', 'answer'
            on_complete: Callback chamado quando todas as perguntas são respondidas
        """
        self.questions = questions
        self.on_complete = on_complete
        self.current_index = 0
        
        # Elementos da UI
        self.question_text = urwid.Text("", wrap='any')
        self.explain_text = urwid.Text("", wrap='any')
        self.prompt_text = urwid.Text(("prompt", "Digite sua resposta e pressione ENTER:"))
        self.answer_edit = urwid.Edit("> ")
        self.feedback_text = urwid.Text("", wrap='any')
        
        # Monta o layout
        self._build_layout()
        
        # Mostra a primeira pergunta
        self._show_current_question()
    
    def _build_layout(self):
        """Constrói o layout da interface."""
        # Cabeçalho
        header = urwid.Pile([
            urwid.Text(("title", "R.A.F.F"), align='center'),
            urwid.Text(("subtitle", "(Rotina de Aprendizado Focada e Flexível)"), align='center'),
            urwid.Divider("─", 1, 1),
        ])
        
        # Coluna da esquerda - Explicação
        left_content = urwid.Pile([
            urwid.Text(("section_title", "Explicação:"), align='center'),
            urwid.Divider(),
            urwid.AttrMap(self.explain_text, "explain_box"),
        ])
        left_box = urwid.LineBox(
            left_content,
            title="[ ! ]",
            tlcorner="┌", tline="─", lline="│", trcorner="┐", rline="│",
            blcorner="└", bline="─", brcorner="┘"
        )
        
        # Coluna da direita - Pergunta e resposta
        right_content = urwid.Pile([
            urwid.Text(("section_title", "Pergunta:"), align='center'),
            urwid.Divider(),
            urwid.AttrMap(self.question_text, "question_box"),
            urwid.Divider(),
            self.prompt_text,
            urwid.AttrMap(self.answer_edit, "edit_box"),
            urwid.Divider(),
            self.feedback_text
        ])
        right_box = urwid.LineBox(
            right_content,
            title="[ ? ]",
            tlcorner="┌", tline="─", lline="│", trcorner="┐", rline="│",
            blcorner="└", bline="─", brcorner="┘"
        )
        
        # Colunas
        columns = urwid.Columns([
            ('weight', 0.5, left_box),
            ('weight', 0.5, right_box)
        ], dividechars=6)
        
        # Layout completo
        body = urwid.Pile([
            header,
            urwid.Divider(),
            columns
        ])
        
        # Janela principal
        main_window = urwid.LineBox(
            urwid.Padding(body, left=2, right=2),
            title="",
            tlcorner="╔", tline="═", trcorner="╗",
            lline="║", rline="║",
            blcorner="╚", bline="═", brcorner="╝"
        )
        
        background = urwid.AttrMap(main_window, "bg")
        
        # Paleta de cores
        palette = [
            ("title", "light magenta,bold", ""),
            ("subtitle", "dark magenta", ""),
            ("section_title", "light magenta,bold", ""),
            ("explain_box", "dark gray", ""),
            ("question_box", "white,bold", ""),
            ("edit_box", "yellow", "black"),
            ("prompt", "yellow,bold", ""),
            ("good", "dark green,bold", ""),
            ("bad", "light red,bold", ""),
        ]
        
        # Loop principal
        self.loop = urwid.MainLoop(
            urwid.Filler(background, valign='top'),
            palette=palette,
            unhandled_input=self._handle_input
        )
    
    def _show_current_question(self):
        """Mostra a pergunta atual."""
        if self.current_index >= len(self.questions):
            self._finish()
            return
        
        q = self.questions[self.current_index]
        self.question_text.set_text(q['question'])
        
        # Formata a explicação (pode ser lista ou string)
        explain = q.get('explain', [])
        if isinstance(explain, list):
            explain_text = '\n'.join(explain)
        else:
            explain_text = explain
        
        self.explain_text.set_text(explain_text)
        self.answer_edit.set_edit_text("")
        self.feedback_text.set_text(
            f"Pergunta {self.current_index + 1}/{len(self.questions)}"
        )
    
    def _handle_input(self, key):
        """Trata entrada do usuário."""
        if key == 'enter':
            self._check_answer()
        elif key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
    
    def _check_answer(self):
        """Verifica a resposta do usuário."""
        user_answer = self.answer_edit.edit_text.strip()
        correct_answer = self.questions[self.current_index]['answer'].strip()
        
        if user_answer.lower() == correct_answer.lower():
            self.feedback_text.set_text(
                ("good", "✔ Correto! Próxima pergunta...")
            )
            self.current_index += 1
            self.loop.set_alarm_in(0.5, lambda loop, data: self._show_current_question())
        else:
            hint = f"{len(correct_answer)} caracteres"
            self.feedback_text.set_text(
                ("bad", f"✖ Errado. Tente novamente. (Dica: {hint})")
            )
    
    def _finish(self):
        """Finaliza o quiz."""
        finish_text = urwid.Text(
            ("good", 
             "🎉 Parabéns! Todas as perguntas foram respondidas!\n\n"
             "Pressione qualquer tecla para continuar..."),
            align='center'
        )
        
        self.loop.widget = urwid.Filler(
            urwid.Padding(finish_text, left=5, right=5),
            valign='middle'
        )
        
        def exit_handler(key):
            raise urwid.ExitMainLoop()
        
        self.loop.unhandled_input = exit_handler
    
    def run(self):
        """Inicia o loop da interface."""
        try:
            self.loop.run()
            # Quando o loop termina, chama o callback
            self.on_complete()
        except urwid.ExitMainLoop:
            self.on_complete()
