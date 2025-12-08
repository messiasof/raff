import requests
import ctypes
import sys
import threading
from modules.fetch import main as fetch_main
from configplaceholder._config import URL, URLCHECK, baseDir, RESPONSAVEL, CHECKCHAR
from modules.varfile import editLastCheckFile

####################################################################################
#              HANDLER PARA CRIAR CONFIRMAÇÃO DE FECHAMENTO DE JANELA              #
####################################################################################

# Necessário manter referência global para evitar GC da função handler
_handler_ref = None

# Tipos para SetConsoleCtrlHandler
HandlerRoutine = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)

# Eventos
CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
CTRL_CLOSE_EVENT = 2
CTRL_LOGOFF_EVENT = 5
CTRL_SHUTDOWN_EVENT = 6

def _show_confirm_message():
    """
    Exibe MessageBox nativo do Windows com 'Sim' e 'Não'.
    Retorna True se o usuário clicar em 'Sim' (quer fechar), False se clicar 'Não'.
    """
    MB_ICONWARNING = 0x30
    MB_YESNO = 0x04
    IDYES = 6
    # Mensagem conforme seu pedido
    texto = (f"Você pode acabar travando o PC e precisando chamar o {RESPONSAVEL} para destravar "
             "se tentar fechar a janela, tem certeza?")
    titulo = "R.A.F.F: Atenção!"
    res = ctypes.windll.user32.MessageBoxW(0, texto, titulo, MB_ICONWARNING | MB_YESNO)
    return res == IDYES

def _console_handler(dwCtrlType):
    """
    Handler chamado pelo Windows quando um evento de console acontece.
    Retorna True se o evento for 'tratado' (ou seja, não deixa o Windows encerrar o processo).
    Retorna False para permitir que o sistema prossiga com o encerramento.
    """
    # Ctrl+C/Ctrl+Break/fechamento da janela.
    if dwCtrlType == CTRL_CLOSE_EVENT:
        # X (fechar janela).
        try:
            # Bloqueia até o usuário responder.
            fechar = _show_confirm_message()
        except Exception:
            # Se a MessageBox falhar por algum motivo, não impedir o fechamento
            return False

        if fechar:
            # Usuário confirmou que quer fechar
            return False  # NÃO trata: permite término normal
        else:
            # CANCELOU: trata tentativa e não deixa fechar o RAFF
            return True

    if dwCtrlType in (CTRL_C_EVENT, CTRL_BREAK_EVENT):
        # Pra configurar conforme o uso: tratar Ctrl+C/Ctrl+Break da mesma forma (ou simplesmente ignorar)
        try:
            fechar = _show_confirm_message()
        except Exception:
            return True  # ignorar por segurança

        if fechar:
            return False
        else:
            return True

    # Para shutdown/logoff - o PC pode ficar travado esperando o programa finalizar. Opcional se você quiser algo mais rígido.
    if dwCtrlType in (CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT):
        return False

    # Default: não tratar
    return False

def install_console_close_confirmation():
    """Instala o handler de console (Windows)."""
    global _handler_ref
    # cria a função com o tipo esperado e guarda referência global
    _handler_ref = HandlerRoutine(_console_handler)
    ok = ctypes.windll.kernel32.SetConsoleCtrlHandler(_handler_ref, True)
    if not ok:
        print("Aviso: falha ao instalar o handler do console (SetConsoleCtrlHandler).")


####################################################################################
#                                 SETUP E EXECUÇÃO                                 #
####################################################################################

def main_program():
    try:
        r = requests.get(URLCHECK, timeout=10)
        r.raise_for_status()
        editLastCheckFile(r.text)
        if r.text == CHECKCHAR:
            fetch_main(URL)
        else:
            pass
    except:
        lastvaluepath = baseDir/".lastcheck"
        with open(lastvaluepath, "r", encoding="utf-8") as file:
            r = file.read()
        if r == CHECKCHAR:
            fetch_main(URL)
        else:
            pass


if __name__ == "__main__":
    # Aviso: O handler só será chamado quando houver tentativa de encerramento
    try:
        main_program()
    except Exception as e:
        print("Erro:", e)
        raise
