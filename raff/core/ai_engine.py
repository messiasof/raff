"""
Módulo de inteligência artificial
Gerencia a geração de perguntas personalizadas usando Gemini com fallback local offline robusto.
"""

from datetime import datetime
import json
import random
from typing import List, Dict, Optional
import requests

from raff.core.config import (
    GEMINI_API_KEY,
    STUDENT_NAME,
    WEEKDAYS,
    AI_QUESTIONS_COUNT,
    MAX_FEEDBACKS,
    AI_FALLBACK_TO_LOCAL,
)
from raff.core.storage import (
    get_feedbacks_text,
    add_feedback,
    save_last_questions,
    get_local_questions,
    get_last_questions,
)


def get_current_subject() -> str:
    """Retorna a matéria do dia baseado no dia da semana."""
    weekday = datetime.today().weekday()
    return WEEKDAYS.get(weekday, "Geral")


def collect_feedback() -> str:
    """Coleta o feedback do responsável via terminal ou interface."""
    materia = get_current_subject()
    print("\n" + "=" * 50)
    print(f"Área do Responsável - Feedback Pedagógico ({materia})")
    print("=" * 50)
    print("Digite suas observações sobre as dificuldades do estudante.")
    print("Isso ajudará a IA a personalizar as próximas perguntas.")
    print("Deixe em branco para pular.\n")

    feedback = input("Feedback: ").strip()

    if feedback:
        add_feedback(feedback)
        print("✅ Feedback salvo com sucesso!")
        return feedback
    else:
        print("Nenhum feedback adicionado.")
        return ""


def get_fallback_questions() -> List[Dict]:
    """
    Obtém perguntas de fallback caso o Gemini esteja inacessível.
    Prioridade:
    1. Perguntas cadastradas localmente pelo responsável
    2. Últimas perguntas salvas em cache (.lastquestions)
    3. Banco padrão interno em pt-BR
    """
    # 1. Tenta pegar do banco local de questões
    local_bank = get_local_questions()
    if local_bank and len(local_bank) > 0:
        return random.sample(local_bank, min(len(local_bank), AI_QUESTIONS_COUNT))

    # 2. Tenta pegar do cache anterior
    last_q = get_last_questions()
    if last_q and len(last_q) > 0:
        return last_q

    # 3. Perguntas estáticas de emergência
    return [
        {
            "id": 1,
            "pergunta": "Quanto é 7 x 8?",
            "opcoes": ["54", "56", "58", "64"],
            "resposta_correta": 1,
            "explicacao": "7 multiplicado por 8 é igual a 56.",
            "materia": "Matemática",
        },
        {
            "id": 2,
            "pergunta": "Qual é a capital do Brasil?",
            "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"],
            "resposta_correta": 2,
            "explicacao": "Brasília é a capital federal do Brasil.",
            "materia": "Geografia",
        },
        {
            "id": 3,
            "pergunta": "Qual palavra está escrita corretamente?",
            "opcoes": ["Exceção", "Exceçâo", "Eceção", "Esseção"],
            "resposta_correta": 0,
            "explicacao": "A grafia correta na língua portuguesa é 'Exceção'.",
            "materia": "Português",
        },
    ]


def generate_questions(
    subject: Optional[str] = None,
    feedbacks: Optional[str] = None,
    student_name: Optional[str] = None,
    teacher_feedback: Optional[str] = None,
) -> List[Dict]:
    """
    Gera perguntas personalizadas usando o modelo Gemini via google-genai.
    Se a API falhar ou estiver sem internet/sem chave, aciona fallback local.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY in ("sua_api_key_aqui", "cole_sua_api_key_aqui"):
        print("⚠️ Chave GEMINI_API_KEY não configurada. Usando fallback local...")
        return get_fallback_questions()

    sub = subject or get_current_subject()
    stu = student_name or STUDENT_NAME
    fbs = feedbacks or get_feedbacks_text()

    if teacher_feedback:
        fbs = f"{fbs}\nFeedback recente do responsável: {teacher_feedback}"

    prompt = f"""
Você é um tutor pedagógico amigável e focado para o estudante {stu}.
Gere {AI_QUESTIONS_COUNT} perguntas de múltipla escolha sobre a matéria '{sub}'.

Histórico pedagógico e observações:
{fbs if fbs else 'Sem observações prévias.'}

Retorne ESTRITAMENTE um JSON no seguinte formato (sem formatação markdown extra fora do json):
[
  {{
    "id": 1,
    "pergunta": "Texto da pergunta?",
    "opcoes": ["Opção A", "Opção B", "Opção C", "Opção D"],
    "resposta_correta": 0,
    "explicacao": "Explicação pedagógica clara e incentivadora",
    "materia": "{sub}"
  }}
]
"""

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        questions = json.loads(text)
        if isinstance(questions, list) and len(questions) > 0:
            save_last_questions(questions)
            return questions
        raise ValueError("Resposta da IA não continha lista válida de perguntas")

    except Exception as e:
        print(f"⚠️ Erro ao conectar com Gemini AI ({e}). Acionando fallback...")
        if AI_FALLBACK_TO_LOCAL:
            return get_fallback_questions()
        raise


def run_ai_feedback_flow() -> List[Dict]:
    """Fluxo para coletar feedback do responsável e gerar as questões."""
    teacher_fb = collect_feedback()
    return generate_questions(teacher_feedback=teacher_fb)
