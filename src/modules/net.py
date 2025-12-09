import subprocess
from pathlib import Path
from src.configplaceholder._config import baseDir
varPath = baseDir/"var.txt" # Define o caminho para o var.txt

def get_var():
    """Lê o conteúdo atual do var.txt."""
    try:
        with open(varPath, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "False"

def checar_adaptador():
        cmd = f"netsh interface show interface"
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.PIPE)
        print(output)

def ligar_desligar(nome): # Precisa de permissão de administrador
    try:
        if get_var() == "True":
            cmd = f'netsh interface set interface "{nome}" admin=disabled'
            subprocess.check_call(cmd, shell=True)
            # DEBUG: #print(f"Internet {nome} desabilitada.")
        else:
            cmd = f'netsh interface set interface "{nome}" admin=enabled'
            subprocess.check_call(cmd, shell=True)
            # DEBUG: #print(f"Internet {nome} habilitada.")
    except subprocess.CalledProcessError as e:
        # DEBUG: #print(f"[ERRO] Falha ao alterar '{nome}': {e}")
        pass
    except PermissionError:
        # DEBUG: #print(f"[ERRO] Permissão negada — execute o script como administrador.")
        pass