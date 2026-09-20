"""
Módulo de configuração do R.A.F.F
Centraliza todas as variáveis de ambiente e preferências do sistema.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env se existir
load_dotenv()

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR = BASE_DIR / "raff" / "gui" / "assets"

# Configurações do Aluno e Responsável
STUDENT_NAME = os.getenv("STUDENT_NAME", "Estudante")
TEACHER_NAME = os.getenv("TEACHER_NAME", "Responsável")

# Modos de Operação
AI_MODE = os.getenv("AI_MODE", "True").lower() in ("true", "1", "yes")
AI_FALLBACK_TO_LOCAL = os.getenv("AI_FALLBACK_TO_LOCAL", "True").lower() in ("true", "1", "yes")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# URLs Legadas / Stubs (Mantidas para retrocompatibilidade)
URL_QUESTIONS = os.getenv("URL_QUESTIONS", "")
URL_CHECK = os.getenv("URL_CHECK", "")
CHECK_CHAR = os.getenv("CHECK_CHAR", "")

# Quantidade de perguntas
AI_QUESTIONS_COUNT = int(os.getenv("AI_QUESTIONS_COUNT", "5"))
MAX_FEEDBACKS = int(os.getenv("MAX_FEEDBACKS", "10"))

# Horários e Agendamento
SCHEDULED_TIMES_RAW = os.getenv("SCHEDULED_TIMES", "10:00,15:00")
SCHEDULED_TIMES = [
    (int(t.split(":")[0]), int(t.split(":")[1]))
    for t in SCHEDULED_TIMES_RAW.split(",")
    if ":" in t
]

# Avisos (Toast Notifications)
START_WARNING_ENABLED = os.getenv("START_WARNING_ENABLED", "True").lower() in ("true", "1", "yes")
START_WARNING_MINUTES = int(os.getenv("START_WARNING_MINUTES", "5"))
START_WARNING_TITLE = os.getenv("START_WARNING_TITLE", "R.A.F.F — Aviso de Foco")
START_WARNING_SOUND = os.getenv("START_WARNING_SOUND", "True").lower() in ("true", "1", "yes")

# Som de Conclusão
default_sound = ASSETS_DIR / "michael-jackson-hee-hee.wav"
COMPLETE_SOUND_PATH = os.getenv("COMPLETE_SOUND_PATH", str(default_sound) if default_sound.exists() else "")

# Adaptadores de Rede
NETWORK_DEVICE_1 = os.getenv("NETWORK_DEVICE_1", "Wi-Fi")
NETWORK_DEVICE_2 = os.getenv("NETWORK_DEVICE_2", "Ethernet")

# Matérias por dia da semana
WEEKDAYS = {
    0: os.getenv("WEEKDAY_0", "Português"),
    1: os.getenv("WEEKDAY_1", "Matemática"),
    2: os.getenv("WEEKDAY_2", "Ciências"),
    3: os.getenv("WEEKDAY_3", "História"),
    4: os.getenv("WEEKDAY_4", "Geografia"),
    5: os.getenv("WEEKDAY_5", "Revisão Geral"),
    6: os.getenv("WEEKDAY_6", "Descanso ou Conhecimentos Gerais"),
}

# Configurações da API REST
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8765"))
