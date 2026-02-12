"""
Módulo principal da aplicação
Contém a lógica de execução do R.A.F.F
"""

import re
import requests
import platform
import os
from typing import List, Dict

from src.config import URL_QUESTIONS, URL_CHECK, CHECK_CHAR, AI_MODE
from src.storage import (
    get_last_questions,
    save_last_questions,
    get_last_check,
    save_last_check,
)
from src.network import disable_network, enable_network
from src.ui import QuizUI
from src.ai_engine import run_ai_feedback_flow


def clear_console():
    """Limpa o console em Windows, Linux e macOS."""
    system_name = platform.system()
    if system_name == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def fetch_remote_content(url: str, timeout: int = 10) -> str:
    """
    Faz fetch de conteúdo remoto.
    
    Args:
        url: URL para fazer o fetch
        timeout: Timeout em segundos
    
    Returns:
        Conteúdo baixado
    
    Raises:
        Exception: Se falhar ao baixar
    """
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text


def should_run_quiz() -> bool:
    """
    Verifica se o quiz deve ser executado baseado no check remoto.
    
    Returns:
        True se deve executar, False caso contrário
    """
    try:
        # Tenta fazer fetch do check remoto
        check_value = fetch_remote_content(URL_CHECK)
        save_last_check(check_value)
        return check_value.strip() == CHECK_CHAR.strip()
    except Exception:
        # Se falhar, usa o último check salvo
        last_check = get_last_check()
        return last_check.strip() == CHECK_CHAR.strip()


def get_questions() -> str:
    """
    Obtém as perguntas para o quiz.
    Se AI_MODE estiver ativado, usa IA. Caso contrário, faz fetch remoto.
    
    Returns:
        String com as perguntas no formato correto
    """
    if AI_MODE:
        # Modo IA: gera perguntas com feedback
        try:
            return run_ai_feedback_flow()
        except Exception as e:
            print(f"Erro ao usar IA: {e}")
            print("Usando perguntas anteriores...\n")
            return get_last_questions()
    else:
        # Modo remoto: faz fetch das perguntas
        try:
            questions_text = fetch_remote_content(URL_QUESTIONS)
            save_last_questions(questions_text)
            return questions_text
        except Exception:
            # Se falhar, usa as últimas perguntas salvas
            return get_last_questions()


def parse_questions(text: str) -> List[Dict]:
    """
    Faz parse das perguntas do formato texto para lista de dicionários.
    
    Formato esperado:
    QUESTION=texto; EXPLAIN=texto; ANSWER=texto;
    
    Args:
        text: Texto com as perguntas
    
    Returns:
        Lista de dicionários com 'question', 'explain', 'answer'
    """
    questions = []
    
    # Remove linhas vazias e processa
    raw_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    
    # Junta tudo e divide por QUESTION=
    full_text = " ".join(raw_lines)
    parts = re.split(r'(?=QUESTION=)', full_text, flags=re.IGNORECASE)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Extrai os campos
        fields = {}
        for match in re.finditer(r'([A-Z]+)\s*=(.*?)\s*(?:;|$)', part, flags=re.IGNORECASE):
            key = match.group(1).strip().upper()
            value = match.group(2).strip()
            fields[key] = value
        
        # Valida que tem os campos necessários
        if 'QUESTION' in fields and 'ANSWER' in fields:
            # Processa o EXPLAIN (converte \\n em quebras de linha reais)
            explain_text = fields.get('EXPLAIN', '').replace("\\n", "\n")
            explain_lines = explain_text.split("\n")
            
            questions.append({
                'question': fields['QUESTION'],
                'explain': explain_lines,
                'answer': fields['ANSWER']
            })
    
    return questions


def on_quiz_complete():
    """Callback chamado quando o quiz é completado."""
    # Reabilita a rede
    enable_network()
    
    # Limpa o console
    clear_console()
    
    print("\n" + "=" * 70)
    print("✅ Quiz completado! Internet reabilitada.")
    print("=" * 70 + "\n")


def run_quiz():
    """
    Executa o quiz completo.
    Desabilita a rede, mostra as perguntas, e reabilita ao finalizar.
    """
    # Obtém as perguntas
    questions_text = get_questions()
    
    if not questions_text:
        print("❌ Erro: Nenhuma pergunta disponível.")
        return
    
    # Faz parse das perguntas
    questions = parse_questions(questions_text)
    
    if not questions:
        print("❌ Erro: Nenhuma pergunta válida encontrada.")
        return
    
    # Desabilita a rede antes de começar
    disable_network()
    
    # Limpa o console
    clear_console()
    
    # Cria e executa a interface
    ui = QuizUI(questions, on_complete=on_quiz_complete)
    ui.run()


def main():
    """
    Função principal da aplicação.
    Verifica se deve executar e roda o quiz.
    """
    # Verifica se deve executar
    if not should_run_quiz():
        print("Quiz não está habilitado no momento.")
        return
    
    # Executa o quiz
    run_quiz()


if __name__ == "__main__":
    main()
