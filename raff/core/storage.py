"""
Módulo de persistência e gerenciamento de armazenamento local
Suporta formato JSON unificado, cache e suporte a dados criptografados.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
import json

from raff.core.config import DATA_DIR, MAX_FEEDBACKS
from raff.core.security import encrypt_data, decrypt_data

# Arquivos de persistência
SETTINGS_PATH = DATA_DIR / "settings.json"
LOCAL_QUESTIONS_PATH = DATA_DIR / "questions.json"
FEEDBACKS_PATH = DATA_DIR / "feedbacks.json"
STATS_PATH = DATA_DIR / "stats.json"

# Legados/Compatibilidade
LASTVALUE_PATH = DATA_DIR / ".lastvalue"
LASTCHECK_PATH = DATA_DIR / ".lastcheck"
LASTQUESTIONS_PATH = DATA_DIR / ".lastquestions"
FEEDBACKS_TXT_PATH = DATA_DIR / ".feedbacks"
NETWORK_STATE_PATH = DATA_DIR / ".network_blocked"


# --- CONFIGURAÇÕES DO SISTEMA (JSON) ---

def load_settings() -> Dict[str, Any]:
    """Carrega as configurações salvas em settings.json."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_settings(settings: Dict[str, Any]) -> None:
    """Salva configurações em settings.json."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


# --- BANCO LOCAL DE QUESTÕES ---

def get_local_questions() -> List[Dict[str, Any]]:
    """Retorna a lista de perguntas cadastradas localmente."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if LOCAL_QUESTIONS_PATH.exists():
        try:
            with open(LOCAL_QUESTIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_local_questions(questions: List[Dict[str, Any]]) -> None:
    """Salva a lista de perguntas no banco local."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOCAL_QUESTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)


def add_local_question(question: Dict[str, Any]) -> None:
    """Adiciona uma pergunta ao banco local."""
    questions = get_local_questions()
    question["id"] = len(questions) + 1
    questions.append(question)
    save_local_questions(questions)


def delete_local_question(question_id: int) -> None:
    """Remove uma pergunta do banco local por ID."""
    questions = [q for q in get_local_questions() if q.get("id") != question_id]
    save_local_questions(questions)


# --- FEEDBACKS PEDAGÓGICOS ---

def get_feedbacks() -> List[Dict[str, str]]:
    """Retorna os feedbacks pedagógicos estruturados."""
    if FEEDBACKS_PATH.exists():
        try:
            with open(FEEDBACKS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    
    # Migra feedback legado se existir
    if FEEDBACKS_TXT_PATH.exists():
        try:
            with open(FEEDBACKS_TXT_PATH, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
                return [{"data": datetime.now().strftime("%d/%m/%Y"), "texto": l} for l in lines]
        except Exception:
            return []
    return []


def add_feedback(feedback_text: str) -> None:
    """Adiciona um feedback pedagógico."""
    if not feedback_text.strip():
        return
    feedbacks = get_feedbacks()
    entry = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "texto": feedback_text.strip()
    }
    feedbacks.append(entry)
    feedbacks = feedbacks[-MAX_FEEDBACKS:]
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(FEEDBACKS_PATH, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=2)


def get_feedbacks_text() -> str:
    """Retorna os feedbacks em texto formatado para envio à IA."""
    feedbacks = get_feedbacks()
    if not feedbacks:
        return ""
    return "\n".join([f"- [{fb.get('data', '')}] {fb.get('texto', '')}" for fb in feedbacks])


# --- ESTATÍSTICAS E DIÁRIO ---

def record_quiz_result(acertos: int, total: int, tempo_segundos: int) -> None:
    """Registra estatísticas de uma sessão concluída de quiz."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stats = {}
    if STATS_PATH.exists():
        try:
            with open(STATS_PATH, "r", encoding="utf-8") as f:
                stats = json.load(f)
        except Exception:
            stats = {}
            
    today = datetime.now().strftime("%Y-%m-%d")
    today_stats = stats.get(today, {"total_quiz": 0, "acertos": 0, "total_perguntas": 0, "tempo_total_segundos": 0})
    
    today_stats["total_quiz"] += 1
    today_stats["acertos"] += acertos
    today_stats["total_perguntas"] += total
    today_stats["tempo_total_segundos"] += tempo_segundos
    
    stats[today] = today_stats
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def get_stats() -> Dict[str, Any]:
    """Retorna as estatísticas agregadas."""
    if STATS_PATH.exists():
        try:
            with open(STATS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


# --- COMPATIBILIDADE LEGADA ---

def get_last_questions() -> List[Dict]:
    if LASTQUESTIONS_PATH.exists():
        try:
            with open(LASTQUESTIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_last_questions(questions: List[Dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(LASTQUESTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)


def get_network_state() -> bool:
    return NETWORK_STATE_PATH.exists()


def save_network_state(blocked: bool) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if blocked:
        NETWORK_STATE_PATH.touch()
    else:
        if NETWORK_STATE_PATH.exists():
            NETWORK_STATE_PATH.unlink()


def get_last_check() -> str:
    if LASTCHECK_PATH.exists():
        try:
            with open(LASTCHECK_PATH, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return ""
    return ""


def save_last_check(check: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(LASTCHECK_PATH, "w", encoding="utf-8") as f:
        f.write(check.strip())
