"""
Módulo de configuração do R.A.F.F
Carrega variáveis de ambiente do arquivo .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Busca o .env automaticamente (subindo diretórios até encontrar)
dotenv_path = find_dotenv(usecwd=True)

if dotenv_path:
    load_dotenv(dotenv_path)
    print(f"✅ Configurações carregadas de: {dotenv_path}")
else:
    print("⚠️  Nenhum arquivo .env encontrado.")
    print("Usando variáveis de ambiente do sistema ou valores padrão.")
    print(f"Crie um .env em: {Path.cwd()}")

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

# Aviso prévio antes de iniciar a atividade
START_WARNING_ENABLED = os.getenv("START_WARNING_ENABLED", "True").lower() in ("true", "1", "yes")
START_WARNING_TITLE = os.getenv("START_WARNING_TITLE", "R.A.F.F")
# Mensagem padrão para aviso interno (durante quiz)
# Para mensagens customizadas, use: python -m src.warn "Sua mensagem aqui"

# Som de conclusão
COMPLETE_SOUND_PATH = os.getenv("COMPLETE_SOUND_PATH", "").strip()

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
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
