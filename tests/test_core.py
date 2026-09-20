"""
Testes unitários dos módulos core do R.A.F.F
"""

import pytest
from raff.core.security import (
    setup_admin_password,
    verify_admin_password,
    encrypt_data,
    decrypt_data,
    hash_password,
    verify_password
)
from raff.core.storage import (
    save_local_questions,
    get_local_questions,
    add_feedback,
    get_feedbacks,
    record_quiz_result,
    get_stats
)
from raff.core.scheduler import RaffScheduler
from raff.core.ai_engine import get_fallback_questions


def test_password_hash_and_verification():
    raw_pwd = "SenhaSecreta@123"
    hashed = hash_password(raw_pwd)
    assert verify_password(raw_pwd, hashed)
    assert not verify_password("SenhaErrada", hashed)


def test_encryption_and_decryption():
    key_pwd = "ChaveAdminMaster"
    plain_text = "Texto altamente sensível do quiz"
    encrypted = encrypt_data(plain_text, key_pwd)
    assert encrypted != plain_text.encode("utf-8")
    decrypted = decrypt_data(encrypted, key_pwd)
    assert decrypted == plain_text


def test_local_questions_storage():
    mock_questions = [
        {"pergunta": "Quanto é 2 + 2?", "opcoes": ["3", "4", "5", "6"], "resposta_correta": 1}
    ]
    save_local_questions(mock_questions)
    loaded = get_local_questions()
    assert len(loaded) >= 1
    assert loaded[0]["pergunta"] == "Quanto é 2 + 2?"


def test_feedbacks_storage():
    add_feedback("Estudante demonstrou ótimo foco hoje.")
    feedbacks = get_feedbacks()
    assert len(feedbacks) >= 1
    assert any("ótimo foco" in f.get("texto", "") for f in feedbacks)


def test_stats_recording():
    record_quiz_result(acertos=5, total=5, tempo_segundos=45)
    stats = get_stats()
    assert len(stats) > 0


def test_scheduler_configuration():
    scheduler = RaffScheduler()
    scheduler.set_schedules([(10, 30), (16, 0)])
    scheduler.set_warning_lead_time(10)
    assert len(scheduler.schedules) == 2
    assert scheduler.warning_minutes == 10


def test_ai_engine_fallback():
    fallback_q = get_fallback_questions()
    assert isinstance(fallback_q, list)
    assert len(fallback_q) > 0
    assert "pergunta" in fallback_q[0]
