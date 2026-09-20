"""
Módulo de gerenciamento de rede
Controla habilitação/desabilitação de adaptadores de rede
"""

import subprocess
from typing import List

from src.config import NETWORK_DEVICE_1, NETWORK_DEVICE_2
from src.storage import save_network_state


def _run_command(command: List[str]) -> bool:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.returncode == 0
    except (OSError, ValueError):
        return False


def toggle_network_adapter(adapter_name: str, enable: bool) -> bool:
    """
    Habilita ou desabilita um adaptador de rede.
    
    Args:
        adapter_name: Nome do adaptador (ex: "Ethernet", "Wi-Fi")
        enable: True para habilitar, False para desabilitar
    
    Returns:
        True se bem-sucedido, False caso contrário
    """
    action = "enabled" if enable else "disabled"
    netsh_command = [
        "netsh",
        "interface",
        "set",
        "interface",
        adapter_name,
        f"admin={action}",
    ]

    if _run_command(netsh_command):
        return True

    powershell_command = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        (
            f"{'Enable' if enable else 'Disable'}-NetAdapter "
            f"-Name '{adapter_name}' -Confirm:$false -ErrorAction Stop"
        ),
    ]

    return _run_command(powershell_command)


def disable_network() -> bool:
    """Desabilita todos os adaptadores de rede configurados."""
    results = [
        toggle_network_adapter(NETWORK_DEVICE_1, False),
        toggle_network_adapter(NETWORK_DEVICE_2, False),
    ]
    save_network_state(disabled=any(results))
    return all(results)


def enable_network() -> bool:
    """Habilita todos os adaptadores de rede configurados."""
    results = [
        toggle_network_adapter(NETWORK_DEVICE_1, True),
        toggle_network_adapter(NETWORK_DEVICE_2, True),
    ]
    save_network_state(disabled=False)
    return all(results)


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
