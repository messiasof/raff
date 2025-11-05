import subprocess
from pathlib import Path
from _config import baseDir

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
        #print(output)

def ligar_desligar(nome): # Requires admin-scope permissions
    try:
        if get_var() == "True":
            cmd = f'netsh interface set interface "{nome}" admin=disabled'
            subprocess.check_call(cmd, shell=True)
            #print(f"Internet {nome} desabilitada.")
        else:
            cmd = f'netsh interface set interface "{nome}" admin=enabled'
            subprocess.check_call(cmd, shell=True)
            #print(f"Internet {nome} habilitada.")
    except subprocess.CalledProcessError as e:
        #print(f"[ERRO] Falha ao alterar '{nome}': {e}")
        pass
    except PermissionError:
        #print(f"[ERRO] Permissão negada — execute o script como administrador.")
        pass

# # def checar_status_adaptador(nome_adaptador):
# #     try:
# #         # Comando WMIC para obter o status do adaptador
# #         cmd = f'wmic nic where "Name=\'{nome_adaptador}\'" get NetEnabled'
# #         output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.PIPE)
        
#         # Analisar a saída para verificar se NetEnabled é True ou False
#        lines = output.strip().split('\n')
#         if len(lines) > 1:
#             status = lines[1].strip()
#             if status == 'TRUE':
#                 return True
#             elif status == 'FALSE':
#                 return False

#     except subprocess.CalledProcessError as e:
#         print(f"Erro ao verificar o status: {e.stderr}")
#         return None
# # Exemplo de uso:
# # Substitua "Wi-Fi" ou "Ethernet" pelo nome exato do seu adaptador de rede
# adaptador_nome = "Wi-Fi" 
# status_ligado = checar_status_adaptador(adaptador_nome)

# if status_ligado is True:
#     print(f"O adaptador '{adaptador_nome}' está LIGADO.")
# elif status_ligado is False:
#     print(f"O adaptador '{adaptador_nome}' está DESLIGADO.")
# else:
#     print(f"Não foi possível determinar o status do adaptador '{adaptador_nome}'.")

# checar_status_adaptador("Teste")

def cicloCompleto():
    checar_adaptador()
    ligar_desligar("Wi-Fi")
    ligar_desligar("Ethernet")
    checar_adaptador()

cicloCompleto()


# fisica udemy e livros
# rafael roblox ask game
# udemy cursos livres
# udemy eletrica
# think40
# python system invading simple
# land rover (trust score)
# fisica para carros
# luta
# aceleração de pensamento
# assistir depois
# screenshots
# rafael documentar pesquisa e depois gerar um texto baseado nos resultados
# eu tinha pensado em alguma coisa tipo "analisar, pensar e escrever", mas o que era? (item acima)
    # fazer isso com pesquisas?
    # fazer isso com plots?
    # passar os plots (el por exemplo) para o notion
# analisar um código e tentar dizer o que as defs fazem pra depois mexer nele