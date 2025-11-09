from pathlib import Path

URL = f""                   # URL onde vai tentar pegar as perguntas, seguindo o padrão QUESTION=text; EXPLAIN=text; ANSWER=text;
URLCHECK = f""              # URL onde ele vai checar remotamente se é para executar o RAFF ou não (defina frequência de execução/checagem no Task Scheduler)
RESPONSAVEL = ""            # Nome do responsável pelo estudante
CHECKCHAR = ""              # Caractere que o programa vai procurar no URLCHECK para servir como "True"


baseDir = Path(__file__).resolve().parent # Definindo o caminho do diretório base (src)

DEVICE1 = "Ethernet" # Mude para o nome do dispositivo de rede que aparece no netsh / Change to network device's name that appears on netsh command
DEVICE2 = "Wi-Fi" # Mude para o nome do dispositivo de rede que aparece no netsh / Change to network device's name that appears on netsh command