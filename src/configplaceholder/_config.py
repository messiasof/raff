# REMOVE THIS IMPORT BELOW
from src.configplaceholder._testing import * # <<< Yeah, that one.
# YEP, THAT ONE ABOVE ^^^

from pathlib import Path

URL = URLBASE                        # URL onde vai tentar pegar as perguntas, seguindo o padrão QUESTION=text; EXPLAIN=text; ANSWER=text;
URLCHECK = URLCHECKING               # URL onde ele vai checar remotamente se é para executar o RAFF ou não (defina frequência de execução/checagem no Task Scheduler)
RESPONSAVEL = TEACHERNAME            # Nome do responsável pelo estudante
CHECKCHAR = CHAR                     # Caractere que o programa vai procurar no URLCHECK para servir como "True"
NAME = STUDENTNAME
GEMINI_APIKEY = APIKEY



baseDir = Path(__file__).resolve().parent # Definindo o caminho do diretório base (src)

DEVICE1 = "Ethernet" # Mude para o nome do dispositivo de rede que aparece no netsh / Change to network device's name that appears on netsh command
DEVICE2 = "Wi-Fi" # Mude para o nome do dispositivo de rede que aparece no netsh / Change to network device's name that appears on netsh command