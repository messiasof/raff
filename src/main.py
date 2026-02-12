"""
R.A.F.F - Rotina de Aprendizado Focada e Flexível
Ponto de entrada principal da aplicação
"""

import ctypes
import sys

from src.config import TEACHER_NAME


# ==========================================
# HANDLER DE FECHAMENTO DE JANELA (WINDOWS)
# ==========================================

_handler_ref = None

HandlerRoutine = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)

# Eventos de console
CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
CTRL_CLOSE_EVENT = 2
CTRL_LOGOFF_EVENT = 5
CTRL_SHUTDOWN_EVENT = 6


def show_close_confirmation():
    """
    Mostra MessageBox nativo do Windows perguntando se realmente quer fechar.
    
    Returns:
        True se o usuário confirmar o fechamento, False caso contrário
    """
    MB_ICONWARNING = 0x30
    MB_YESNO = 0x04
    IDYES = 6
    
    text = (
        f"Você pode acabar travando o PC e precisando chamar o {TEACHER_NAME} "
        "para destravar se tentar fechar a janela, tem certeza?"
    )
    title = "R.A.F.F: Atenção!"
    
    result = ctypes.windll.user32.MessageBoxW(0, text, title, MB_ICONWARNING | MB_YESNO)
    return result == IDYES


def console_handler(dwCtrlType):
    """
    Handler chamado pelo Windows quando um evento de console acontece.
    
    Returns:
        True se o evento for tratado (bloqueia o fechamento)
        False para permitir o fechamento
    """
    if dwCtrlType == CTRL_CLOSE_EVENT:
        # Usuário tentou fechar a janela
        try:
            should_close = show_close_confirmation()
        except Exception:
            return False
        
        if should_close:
            return False  # Permite fechar
        else:
            return True  # Bloqueia o fechamento
    
    if dwCtrlType in (CTRL_C_EVENT, CTRL_BREAK_EVENT):
        # Ctrl+C ou Ctrl+Break
        try:
            should_close = show_close_confirmation()
        except Exception:
            return True
        
        if should_close:
            return False
        else:
            return True
    
    # Shutdown/Logoff - permite para não travar o sistema
    if dwCtrlType in (CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT):
        return False
    
    return False


def install_close_handler():
    """Instala o handler de fechamento de console (Windows)."""
    global _handler_ref
    
    try:
        _handler_ref = HandlerRoutine(console_handler)
        success = ctypes.windll.kernel32.SetConsoleCtrlHandler(_handler_ref, True)
        
        if not success:
            print("⚠ Aviso: Não foi possível instalar o handler de fechamento.")
    except Exception as e:
        print(f"⚠ Aviso: Erro ao instalar handler de fechamento: {e}")


# ==========================================
# MAIN
# ==========================================

def main():
    """Função principal."""
    # Instala o handler de fechamento (apenas Windows)
    if sys.platform == "win32":
        install_close_handler()
    
    # Importa e executa a aplicação
    try:
        from src.app import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
