"""
Módulo de gerenciamento de rede
Controla habilitação/desabilitação de adaptadores de rede
"""

import subprocess
from typing import List

from src.config import NETWORK_DEVICE_1, NETWORK_DEVICE_2
from src.storage import save_network_state


def toggle_network_adapter(adapter_name: str, enable: bool) -> bool:
    """
    Habilita ou desabilita um adaptador de rede.
    
    Args:
        adapter_name: Nome do adaptador (ex: "Ethernet", "Wi-Fi")
        enable: True para habilitar, False para desabilitar
    
    Returns:
        True se bem-sucedido, False caso contrário
    """
    try:
        action = "enabled" if enable else "disabled"
        cmd = f'netsh interface set interface "{adapter_name}" admin={action}'
        subprocess.check_call(cmd, shell=True, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, PermissionError):
        return False


def disable_network() -> None:
    """Desabilita todos os adaptadores de rede configurados."""
    toggle_network_adapter(NETWORK_DEVICE_1, False)
    toggle_network_adapter(NETWORK_DEVICE_2, False)
    save_network_state(disabled=True)


def enable_network() -> None:
    """Habilita todos os adaptadores de rede configurados."""
    toggle_network_adapter(NETWORK_DEVICE_1, True)
    toggle_network_adapter(NETWORK_DEVICE_2, True)
    save_network_state(disabled=False)


def list_network_adapters() -> List[str]:
    """
    Lista todos os adaptadores de rede disponíveis.
    Útil para debug e configuração.
    """
    try:
        cmd = "netsh interface show interface"
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        return output.splitlines()
    except subprocess.CalledProcessError:
        return []
