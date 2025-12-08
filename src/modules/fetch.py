import sys
import requests
import urwid
import re
import os
import platform
from src.modules.varfile import editVarFile, editLastValueFile, lastvaluepath
from src.modules.net import ligar_desligar
from src.configplaceholder._config import DEVICE1, DEVICE2, baseDir

def clear_console():
    #Limpa o console em Windows, Linux e macOS
    system_name = platform.system()
    if system_name == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# -------- Funções de rede e parsing ----------
def fetch_text(url, timeout=10):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        editLastValueFile(r.text)
        return r.text
    except:
        with open(lastvaluepath, "r", encoding="utf-8") as file:
            r = file.read() #.strip()
            return r

def parse_entries(text):
    entries = []
    raw_lines = [ln.strip() for ln in text.splitlines()]
    buffer = []
    for ln in raw_lines:
        if ln == "":
            if buffer:
                entries.extend(_parse_lines_as_entries(buffer))
                buffer = []
        else:
            buffer.append(ln)
    if buffer:
        entries.extend(_parse_lines_as_entries(buffer))
    return entries

def _parse_lines_as_entries(lines):
    joined = " ".join(lines)
    parts = re.split(r'(?=QUESTION=)', joined, flags=re.IGNORECASE)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        fields = {}
        for m in re.finditer(r'([A-Z]+)\s*=(.*?)\s*(?:;|$)', p, flags=re.IGNORECASE):
            key = m.group(1).strip().upper()
            val = m.group(2).strip()
            fields[key] = val
        if 'QUESTION' in fields and 'ANSWER' in fields:
            explain_text = fields.get('EXPLAIN', '').replace("\\n", "\n")  # Substitui as \n por quebras de linha
            explain_lines = explain_text.split("\n")
            out.append({
                'question': fields.get('QUESTION', ''),
                'explain': explain_lines,  # Agora 'explain' será uma lista de linhas
                'answer': fields.get('ANSWER', '')
            })
    editVarFile("True")
    #ligar_desligar(DEVICE1)
    #ligar_desligar(DEVICE2)
    clear_console()
    return out


# -------- Interface com urwid ----------
class QuizUI:
    def __init__(self, entries):
        self.entries = entries
        self.index = 0

        # Elementos principais
        self.question = urwid.Text("", wrap='any')
        self.explain = urwid.Text("", wrap='any')
        self.prompt = urwid.Text(("prompt", "Digite sua resposta e pressione ENTER:"))
        self.edit = urwid.Edit("> ")
        self.feedback = urwid.Text("", wrap='any')

        # Cabeçalho com cor roxa
        header = urwid.Pile([
            urwid.Text(("title", "R.A.F.F"), align='center'),
            urwid.Text(("subtitle", "(Rotina de Aprendizado Focada e Flexível)"), align='center'),
            urwid.Divider("─", 1, 1),
        ])

        # Coluna da esquerda — explicação
        left_content = urwid.Pile([
            urwid.Text(("section_title", "Explicação:"), align='center'),
            urwid.Divider(),
            urwid.AttrMap(self.explain, "explain_box"),
        ])
        left_box = urwid.LineBox(
            left_content, title="[ ! ]", tlcorner="┌", tline="─", lline="│", trcorner="┐", rline="│",
            blcorner="└", bline="─", brcorner="┘"
        )

        # Coluna da direita — pergunta + resposta
        right_content = urwid.Pile([
            urwid.Text(("section_title", "Pergunta:"), align='center'),
            urwid.Divider(),
            urwid.AttrMap(self.question, "question_box"),
            urwid.Divider(),
            self.prompt,
            urwid.AttrMap(self.edit, "edit_box"),
            urwid.Divider(),
            self.feedback
        ])
        right_box = urwid.LineBox(
            right_content, title="[ ? ]", tlcorner="┌", tline="─", lline="│", trcorner="┐", rline="│",
            blcorner="└", bline="─", brcorner="┘"
        )

        # Colunas — com mais espaçamento entre elas
        columns = urwid.Columns([
            ('weight', 0.5, left_box),
            ('weight', 0.5, right_box)
        ], dividechars=6)  # << espaçamento entre colunas

        # Layout completo
        body = urwid.Pile([
            header,
            urwid.Divider(),
            columns
        ])

        # Mega janela que engloba tudo
        main_window = urwid.LineBox(
            urwid.Padding(body, left=2, right=2),
            title="",
            tlcorner="╔", tline="═", trcorner="╗",
            lline="║", rline="║",
            blcorner="╚", bline="═", brcorner="╝"
        )

        # Fundo colorido (opcional: dark gray ou roxo escuro)
        background = urwid.AttrMap(main_window, "bg")

        # Paleta de cores
        palette = [
            (f"title", "light magenta,bold", ""),          # R.A.F.F — roxo forte
            (f"subtitle", "dark magenta", ""),             # subtexto — roxo mais escuro
            (f"section_title", "light magenta,bold", ""),  # Títulos (Pergunta / Explicação)
            (f"explain_box", "dark gray", ""),             # Texto de explicação (cinza)
            (f"question_box", "white,bold", ""),           # Texto da pergunta (branco)
            (f"edit_box", "yellow", "black"),              # Campo de resposta (amarelo)
            (f"prompt", "yellow,bold", ""),                # Texto de orientação (amarelo)
            (f"good", "dark green,bold", ""),
            (f"bad", "light red,bold", "")
        ]

        # Loop principal
        self.loop = urwid.MainLoop(
            urwid.Filler(background, valign='top'),
            palette=palette,
            unhandled_input=self.unhandled_input
        )

        self.show_current()

    # --------- Lógica principal ----------
    def show_current(self):
        if self.index >= len(self.entries):
            self.finish()
            return
        e = self.entries[self.index]
        self.question.set_text(e['question'])
        # Agora passamos uma lista de strings para o urwid.Text
        self.explain.set_text('\n'.join(e.get('explain', [])))
        self.edit.set_edit_text("")
        self.feedback.set_text(f"Pergunta {self.index+1}/{len(self.entries)}")

    def unhandled_input(self, key):
        if key == 'enter':
            self.check_answer()
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def check_answer(self):
        user = self.edit.edit_text.strip()
        correct = self.entries[self.index]['answer'].strip()
        if user.lower() == correct.lower():
            self.feedback.set_text(("good", "✔ Correto! Próxima pergunta..."))
            self.index += 1
            self.show_current()
        else:
            self.feedback.set_text(("bad", f"✖ Errado. Tente novamente. ({len(correct)} letras)"))
            self.loop.draw_screen()

    def finish(self):
        txt = urwid.Text(("good", "🎉 Parabéns! Todas as perguntas foram respondidas!\nPressione qualquer tecla para sair."))
        self.loop.widget = urwid.Filler(urwid.Pile([txt]))
        self.loop.unhandled_input = lambda k: (_ for _ in ()).throw(urwid.ExitMainLoop())
        editVarFile("False")
        ligar_desligar(DEVICE1)
        ligar_desligar(DEVICE2)

    def run(self):
        self.loop.run()

# --------- main ----------
def main(arg=None):
    if len(sys.argv) > 1:
        print("Uso: python raff.py <URL_do_arquivo_txt>")
        url = sys.argv[1]
    elif arg:
        url = arg
    else:
        sys.exit(1)
    try:
        text = fetch_text(url)
    except Exception as e:
        print("Erro ao baixar o arquivo:", e)
        sys.exit(1)
    entries = parse_entries(text)
    if not entries:
        print("Nenhuma entrada válida encontrada no arquivo.")
        sys.exit(1)

    ui = QuizUI(entries)
    ui.run()

if __name__ == "__main__":
    main()