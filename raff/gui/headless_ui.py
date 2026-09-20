"""
Interface CLI (modo headless) do R.A.F.F usando urwid
Modo de retrocompatibilidade ativado com `raff start --headless`
"""

from typing import List, Dict, Callable

try:
    import urwid  # type: ignore
    URWID_AVAILABLE = True
except ImportError:
    URWID_AVAILABLE = False


def _format_question_text(q: Dict) -> str:
    """Extrai o texto da pergunta do formato novo (pergunta) ou legado (question)."""
    return q.get("pergunta", q.get("question", ""))


def _format_options_text(q: Dict) -> str:
    """Formata as opções de múltipla escolha, ou retorna explicação legada."""
    opcoes = q.get("opcoes", [])
    if opcoes and len(opcoes) > 1:
        labels = ["a)", "b)", "c)", "d)", "e)"]
        linhas = [f"{labels[i]} {opt}" for i, opt in enumerate(opcoes)]
        return "\n".join(linhas)
    # Formato legado: explain como lista ou string
    explain = q.get("explain", q.get("explicacao", ""))
    if isinstance(explain, list):
        return "\n".join(explain)
    return str(explain)


def _get_correct_answer(q: Dict) -> str:
    """Retorna a resposta correta normalizada para comparação."""
    opcoes = q.get("opcoes", [])
    if opcoes and len(opcoes) > 1:
        idx = q.get("resposta_correta", 0)
        labels = ["a", "b", "c", "d", "e"]
        return labels[idx] if idx < len(labels) else str(idx)
    # Formato legado
    return str(q.get("answer", q.get("resposta_correta", ""))).strip()


class QuizUI:
    """Interface de quiz em modo terminal (headless) usando urwid."""

    def __init__(self, questions: List[Dict], on_complete: Callable):
        self.questions = questions
        self.on_complete = on_complete
        self.current_index = 0

        if not URWID_AVAILABLE:
            self._run_simple()
            return

        self.question_text = urwid.Text("", wrap="any")
        self.explain_text = urwid.Text("", wrap="any")
        self.prompt_text = urwid.Text(("prompt", "Digite a resposta e pressione ENTER:"))
        self.answer_edit = urwid.Edit("> ")
        self.feedback_text = urwid.Text("", wrap="any")

        self._build_layout()
        self._show_current_question()

    def _build_layout(self):
        header = urwid.Pile([
            urwid.Text(("title", "R.A.F.F"), align="center"),
            urwid.Text(("subtitle", "Rotina de Aprendizado e Foco Familiar"), align="center"),
            urwid.Divider("-"),
        ])

        left_content = urwid.Pile([
            urwid.Text(("section_title", "Explicação:"), align="center"),
            urwid.Divider(),
            urwid.AttrMap(self.explain_text, "explain_box"),
        ])
        left_box = urwid.LineBox(left_content, title="[ ! ]")

        right_content = urwid.Pile([
            urwid.Text(("section_title", "Pergunta:"), align="center"),
            urwid.Divider(),
            urwid.AttrMap(self.question_text, "question_box"),
            urwid.Divider(),
            self.prompt_text,
            urwid.AttrMap(self.answer_edit, "edit_box"),
            urwid.Divider(),
            self.feedback_text,
        ])
        right_box = urwid.LineBox(right_content, title="[ ? ]")

        columns = urwid.Columns([
            ("weight", 0.5, left_box),
            ("weight", 0.5, right_box),
        ], dividechars=4)

        body = urwid.Pile([header, urwid.Divider(), columns])
        background = urwid.AttrMap(urwid.LineBox(urwid.Padding(body, left=2, right=2)), "bg")

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
            ("bg", "", ""),
        ]

        self.loop = urwid.MainLoop(
            urwid.Filler(background, valign="top"),
            palette=palette,
            unhandled_input=self._handle_input,
        )

    def _show_current_question(self):
        if self.current_index >= len(self.questions):
            self._finish()
            return

        q = self.questions[self.current_index]
        self.question_text.set_text(_format_question_text(q))
        self.explain_text.set_text(_format_options_text(q))
        self.answer_edit.set_edit_text("")
        self.feedback_text.set_text(
            f"Pergunta {self.current_index + 1} de {len(self.questions)}"
        )

    def _handle_input(self, key):
        if key == "enter":
            self._check_answer()
        elif key in ("q", "Q"):
            raise urwid.ExitMainLoop()

    def _check_answer(self):
        user_answer = self.answer_edit.edit_text.strip().lower()
        correct = _get_correct_answer(self.questions[self.current_index]).lower()

        if user_answer == correct:
            self.feedback_text.set_text(("good", "✔ Correto! Próxima pergunta..."))
            self.current_index += 1
            self.loop.set_alarm_in(0.5, lambda loop, data: self._show_current_question())
        else:
            hint = f"{len(correct)} caractere(s)"
            self.feedback_text.set_text(("bad", f"✖ Errado. Tente novamente. (Dica: {hint})"))

    def _finish(self):
        finish_text = urwid.Text(
            ("good", "Parabéns! Todas as perguntas foram respondidas!\n\nPressione qualquer tecla para sair."),
            align="center",
        )
        self.loop.widget = urwid.Filler(urwid.Padding(finish_text, left=5, right=5), valign="middle")
        self.loop.unhandled_input = lambda key: (_ for _ in ()).throw(urwid.ExitMainLoop())

    def run(self):
        if not URWID_AVAILABLE:
            return
        try:
            self.loop.run()
            self.on_complete()
        except urwid.ExitMainLoop:
            self.on_complete()

    def _run_simple(self):
        """Fallback sem urwid — loop input básico no terminal."""
        print("\nR.A.F.F — Modo Terminal (urwid não instalado)\n")
        for i, q in enumerate(self.questions):
            print(f"\nPergunta {i + 1}/{len(self.questions)}: {_format_question_text(q)}")
            opts = _format_options_text(q)
            if opts:
                print(opts)
            correct = _get_correct_answer(q).lower()
            while True:
                resp = input("Sua resposta: ").strip().lower()
                if resp == correct:
                    print("✔ Correto!")
                    break
                else:
                    print(f"✖ Errado. Tente novamente.")
        print("\nParabéns! Todas as perguntas foram respondidas!")
        self.on_complete()
