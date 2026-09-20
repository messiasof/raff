"""
Módulo principal da aplicação
Contém a lógica de orquestração do R.A.F.F
"""

import os
import platform
from pathlib import Path
from typing import List, Dict, Optional

from raff.core.config import (
    URL_QUESTIONS,
    URL_CHECK,
    CHECK_CHAR,
    AI_MODE,
    COMPLETE_SOUND_PATH,
)
from raff.core.storage import (
    get_last_questions,
    save_last_questions,
    get_last_check,
    save_last_check,
    get_network_state,
    get_local_questions,
)
from raff.core.network import disable_network, enable_network
from raff.core.ai_engine import run_ai_feedback_flow, generate_questions, get_fallback_questions


def clear_console():
    """Limpa o console em Windows, Linux e macOS."""
    os.system("cls" if platform.system() == "Windows" else "clear")


def fetch_remote_content(url: str, timeout: int = 10) -> str:
    """Faz fetch de conteúdo remoto."""
    import requests
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text


def play_completion_sound() -> None:
    """Toca um som opcional ao terminar a atividade."""
    if not COMPLETE_SOUND_PATH or platform.system() != "Windows":
        return
    sound_path = Path(COMPLETE_SOUND_PATH).expanduser()
    if not sound_path.exists():
        return
    try:
        import winsound
        winsound.PlaySound(
            str(sound_path),
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
        )
    except Exception:
        pass


def should_run_quiz() -> bool:
    """
    Verifica se o quiz deve ser executado.
    Se URL_CHECK estiver configurado, consulta remotamente.
    Caso contrário, retorna True (sem controle remoto).
    """
    if not URL_CHECK:
        return True
    try:
        check_value = fetch_remote_content(URL_CHECK)
        save_last_check(check_value)
        return check_value.strip() == CHECK_CHAR.strip()
    except Exception:
        last_check = get_last_check()
        if not last_check:
            return True
        return last_check.strip() == CHECK_CHAR.strip()


def get_questions() -> List[Dict]:
    """
    Obtém questões com a seguinte prioridade:
    1. Gemini AI (se AI_MODE=True e chave configurada)
    2. Questões locais cadastradas
    3. URL remota (stub legado, se URL_QUESTIONS configurado)
    4. Cache da última sessão
    5. Banco de emergência interno
    """
    if AI_MODE:
        try:
            return run_ai_feedback_flow()
        except Exception as e:
            print(f"Aviso: IA indisponível ({e}). Usando fallback local...")

    # Questões locais cadastradas
    local = get_local_questions()
    if local:
        return local

    # URL remota legada (stub)
    if URL_QUESTIONS:
        try:
            import re
            text = fetch_remote_content(URL_QUESTIONS)
            parsed = parse_text_questions(text)
            if parsed:
                save_last_questions(parsed)
                return parsed
        except Exception:
            pass

    # Cache da última sessão
    cached = get_last_questions()
    if cached:
        return cached

    # Banco de emergência
    return get_fallback_questions()


def parse_text_questions(text: str) -> List[Dict]:
    """
    Faz parse do formato legado de questões (Pastebin).
    Formato: QUESTION=texto; EXPLAIN=texto; ANSWER=texto;
    """
    import re
    questions = []
    raw_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    full_text = " ".join(raw_lines)
    parts = re.split(r'(?=QUESTION=)', full_text, flags=re.IGNORECASE)

    for part in parts:
        part = part.strip()
        if not part:
            continue
        fields = {}
        for match in re.finditer(r'([A-Z]+)\s*=(.*?)\s*(?:;|$)', part, flags=re.IGNORECASE):
            key = match.group(1).strip().upper()
            value = match.group(2).strip()
            fields[key] = value

        if 'QUESTION' in fields and 'ANSWER' in fields:
            explain_text = fields.get('EXPLAIN', '').replace("\\n", "\n")
            questions.append({
                'pergunta': fields['QUESTION'],
                'opcoes': [fields['ANSWER']],
                'resposta_correta': 0,
                'explicacao': explain_text,
                'materia': 'Geral',
            })
    return questions


def on_quiz_complete():
    """Callback chamado quando o quiz é completado no modo headless."""
    enable_network()
    play_completion_sound()
    clear_console()
    print("\n" + "=" * 70)
    print("Parabéns! Quiz concluído com sucesso. Internet reabilitada.")
    print("=" * 70 + "\n")


def run_headless_quiz():
    """
    Executa o quiz em modo CLI/headless (urwid).
    Usado pelo comando `raff start --headless`.
    """
    questions = get_questions()

    if not questions:
        print("Nenhuma pergunta disponível para a sessão.")
        return

    network_disabled = disable_network()
    if not network_disabled:
        print("Aviso: Não foi possível desabilitar a rede. Sessão encerrada.")
        enable_network()
        return

    clear_console()

    try:
        from raff.gui.headless_ui import QuizUI
        ui = QuizUI(questions, on_complete=on_quiz_complete)
        ui.run()
    finally:
        if get_network_state():
            enable_network()


def run_gui_quiz():
    """
    Executa o quiz em modo GUI (PyQt6).
    Usado pelo tray app e pelo comando `raff start` sem --headless.
    """
    questions = get_questions()
    if not questions:
        return None
    disable_network()
    return questions


def main():
    """Ponto de entrada para o modo headless (raff start --headless)."""
    if not should_run_quiz():
        print("Quiz não habilitado para este momento.")
        return
    run_headless_quiz()


if __name__ == "__main__":
    main()
