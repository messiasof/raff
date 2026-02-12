"""
Módulo de configuração do R.A.F.F
Carrega variáveis de ambiente do arquivo .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega o .env da raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    raise FileNotFoundError(
        f"Arquivo .env não encontrado em {ENV_PATH}.\n"
        "Por favor, copie o .env.example para .env e configure suas variáveis."
    )

# URLs de controle
URL_QUESTIONS = os.getenv("URL_QUESTIONS")
URL_CHECK = os.getenv("URL_CHECK")
CHECK_CHAR = os.getenv("CHECK_CHAR")

# Informações pessoais
STUDENT_NAME = os.getenv("STUDENT_NAME", "Estudante")
TEACHER_NAME = os.getenv("TEACHER_NAME", "Responsável")

# API da IA
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Modo IA
AI_MODE = os.getenv("AI_MODE", "True").lower() in ("true", "1", "yes")

# Adaptadores de rede
NETWORK_DEVICE_1 = os.getenv("NETWORK_DEVICE_1", "Ethernet")
NETWORK_DEVICE_2 = os.getenv("NETWORK_DEVICE_2", "Wi-Fi")

# Matérias por dia da semana
WEEKDAYS = {
    0: os.getenv("WEEKDAY_0", "Português"),
    1: os.getenv("WEEKDAY_1", "Português"),
    2: os.getenv("WEEKDAY_2", "Matemática"),
    3: os.getenv("WEEKDAY_3", "Matemática"),
    4: os.getenv("WEEKDAY_4", "Matemática"),
    5: os.getenv("WEEKDAY_5", "Inglês"),
    6: os.getenv("WEEKDAY_6", "Inglês"),
}

# Quantidade de perguntas
AI_QUESTIONS_COUNT = int(os.getenv("AI_QUESTIONS_COUNT", "3"))

# Quantidade máxima de feedbacks
MAX_FEEDBACKS = int(os.getenv("MAX_FEEDBACKS", "10"))

# Diretórios
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
