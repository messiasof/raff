"""
Módulo de gerenciamento de armazenamento local
Gerencia arquivos de persistência (.lastvalue, .lastcheck, .lastfeedback, etc.)
"""

from pathlib import Path
from typing import List, Optional
import json

from src.config import DATA_DIR

# Arquivos de persistência
LASTVALUE_PATH = DATA_DIR / ".lastvalue"
LASTCHECK_PATH = DATA_DIR / ".lastcheck"
FEEDBACKS_PATH = DATA_DIR / ".feedbacks.json"
NETWORK_STATE_PATH = DATA_DIR / ".network_state"


def read_file(path: Path, default: str = "") -> str:
    """Lê conteúdo de um arquivo, retorna default se não existir."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return default


def write_file(path: Path, content: str) -> None:
    """Escreve conteúdo em um arquivo."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ===== Gerenciamento de perguntas =====

def get_last_questions() -> str:
    """Retorna as últimas perguntas armazenadas."""
    return read_file(LASTVALUE_PATH)


def save_last_questions(content: str) -> None:
    """Salva as perguntas baixadas."""
    write_file(LASTVALUE_PATH, content.strip())


# ===== Gerenciamento de check =====

def get_last_check() -> str:
    """Retorna o último valor de check."""
    return read_file(LASTCHECK_PATH)


def save_last_check(content: str) -> None:
    """Salva o último valor de check."""
    write_file(LASTCHECK_PATH, content.strip())


# ===== Gerenciamento de feedbacks =====

def get_feedbacks(max_count: Optional[int] = None) -> List[str]:
    """
    Retorna lista de feedbacks armazenados.
    Se max_count for especificado, retorna apenas os últimos N feedbacks.
    """
    try:
        with open(FEEDBACKS_PATH, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)
        if max_count:
            return feedbacks[-max_count:]
        return feedbacks
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def add_feedback(feedback: str, max_feedbacks: int = 10) -> None:
    """
    Adiciona um novo feedback à lista.
    Mantém apenas os últimos max_feedbacks feedbacks.
    """
    feedbacks = get_feedbacks()
    feedbacks.append(feedback)
    
    # Remove feedbacks antigos se ultrapassar o limite
    if len(feedbacks) > max_feedbacks:
        feedbacks = feedbacks[-max_feedbacks:]
    
    with open(FEEDBACKS_PATH, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=2)


def get_feedbacks_text(max_count: Optional[int] = None) -> str:
    """Retorna feedbacks formatados como texto."""
    feedbacks = get_feedbacks(max_count)
    if not feedbacks:
        return "Nenhum feedback anterior."
    
    text = []
    for i, feedback in enumerate(feedbacks, 1):
        text.append(f"{i}. {feedback}")
    return "\n".join(text)


# ===== Gerenciamento de estado de rede =====

def get_network_state() -> bool:
    """
    Retorna True se a rede está desabilitada, False se está habilitada.
    """
    state = read_file(NETWORK_STATE_PATH, "enabled")
    return state == "disabled"


def save_network_state(disabled: bool) -> None:
    """
    Salva o estado da rede.
    disabled=True significa que a rede está bloqueada.
    """
    write_file(NETWORK_STATE_PATH, "disabled" if disabled else "enabled")
