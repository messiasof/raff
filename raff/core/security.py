"""
Módulo de segurança e proteção por senha do R.A.F.F
Gerencia hashing, verificação de senha do administrador e criptografia simétrica de dados sensíveis.
"""

import os
import base64
from pathlib import Path
from typing import Optional, Tuple
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from raff.core.config import DATA_DIR

ADMIN_HASH_FILE = DATA_DIR / ".admin_hash"
FERNET_SALT_FILE = DATA_DIR / ".fernet_salt"

AVISO_SEM_RECUPERACAO = "IMPORTANTE: Anote sua senha em local seguro. Não há mecanismo de recuperação ou reset de senha."


def hash_password(plain: str) -> bytes:
    """Gera hash seguro bcrypt para a senha."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain.encode("utf-8"), salt)


def verify_password(plain: str, hashed: bytes) -> bool:
    """Verifica se a senha em texto puro confere com o hash bcrypt."""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed)
    except Exception:
        return False


def setup_admin_password(plain: str) -> bool:
    """Configura e salva a senha do administrador pela primeira vez ou alteração autorizada."""
    if not plain or not plain.strip():
        raise ValueError("A senha não pode ser vazia.")
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    hashed = hash_password(plain.strip())
    
    with open(ADMIN_HASH_FILE, "wb") as f:
        f.write(hashed)
        
    # Inicializa o salt para derivação do Fernet se não existir
    if not FERNET_SALT_FILE.exists():
        salt = os.urandom(16)
        with open(FERNET_SALT_FILE, "wb") as f:
            f.write(salt)
            
    return True


def is_admin_password_set() -> bool:
    """Verifica se a senha de administrador já está configurada."""
    return ADMIN_HASH_FILE.exists() and ADMIN_HASH_FILE.stat().st_size > 0


def verify_admin_password(plain: str) -> bool:
    """Valida a senha contra o hash salvo no disco."""
    if not is_admin_password_set():
        return False
    try:
        with open(ADMIN_HASH_FILE, "rb") as f:
            hashed = f.read().strip()
        return verify_password(plain, hashed)
    except Exception:
        return False


def _get_or_create_salt() -> bytes:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if FERNET_SALT_FILE.exists() and FERNET_SALT_FILE.stat().st_size > 0:
        with open(FERNET_SALT_FILE, "rb") as f:
            return f.read()
    salt = os.urandom(16)
    with open(FERNET_SALT_FILE, "wb") as f:
        f.write(salt)
    return salt


def generate_fernet_key_from_password(plain_password: str) -> bytes:
    """Deriva chave Fernet de 32 bytes URL-safe a partir da senha e salt usando PBKDF2."""
    salt = _get_or_create_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(plain_password.encode("utf-8")))
    return key


def encrypt_data(data_str: str, plain_password: str) -> bytes:
    """Criptografa uma string usando a senha fornecida."""
    if not data_str:
        return b""
    key = generate_fernet_key_from_password(plain_password)
    f = Fernet(key)
    return f.encrypt(data_str.encode("utf-8"))


def decrypt_data(encrypted_bytes: bytes, plain_password: str) -> str:
    """Descriptografa bytes cifrados usando a senha fornecida."""
    if not encrypted_bytes:
        return ""
    try:
        key = generate_fernet_key_from_password(plain_password)
        f = Fernet(key)
        return f.decrypt(encrypted_bytes).decode("utf-8")
    except Exception:
        return ""


def require_admin_password(plain_password: str) -> bool:
    """Valida se a senha informada concede acesso de administrador."""
    return verify_admin_password(plain_password)
