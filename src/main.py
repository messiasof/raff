"""
Módulo de gerenciamento de fechamento seguro
Previnindo fechamento acidental com restauração automática
"""

import atexit
import sys
import time
from threading import Thread

from src.network import enable_network, disable_network
from src.storage import get_network_state, save_network_state


def restore_network_if_needed():
    """Restaura a rede ao encerrar o processo, se ela tiver sido bloqueada."""
    try:
        if get_network_state():
            enable_network()
    except Exception:
        pass


def prevent_close():
    """Loop infinito que previne fechamento acidental."""
    while True:
        try:
            time.sleep(0.5)
            # Verifica se o programa está em execução
            if sys.platform != "win32":
                continue
                
            # Força o bloqueio de fechamento
            import ctypes
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 
                0  # Minimiza a janela para forçar o fechamento
            )
            
        except Exception:
            pass


def install_close_prevention():
    """Instala o bloqueio de fechamento e restauração."""
    # Cria thread para bloqueio de fechamento
    Thread(target=prevent_close, daemon=True).start()
    
    # Registra restauração ao sair (de emergência, se rede estiver bloqueada)
    atexit.register(restore_network_if_needed)


# ==========================================
# PONTO DE ENTRADA PRINCIPAL
# ==========================================

def main():
    """Função principal com bloqueio de fechamento."""
    try:
        # Instala o bloqueio de fechamento
        install_close_prevention()
        
        # Importa e executa a aplicação
        from src.app import main as app_main
        app_main()
        
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
        restore_network_if_needed()
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        restore_network_if_needed()
        sys.exit(1)


if __name__ == "__main__":
    main()