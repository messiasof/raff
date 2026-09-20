"""
API REST Local/LAN do R.A.F.F com FastAPI
Permite ao responsável acompanhar métricas, adicionar questões e disparar quiz remotamente.
"""

from typing import List, Dict, Optional, Any
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

from raff.core.config import API_HOST, API_PORT, STUDENT_NAME, TEACHER_NAME
from raff.core.security import verify_admin_password
from raff.core.storage import (
    get_local_questions, add_local_question, get_stats, get_feedbacks, add_feedback
)
from raff.core.network import get_network_state, enable_network, disable_network

app = FastAPI(
    title="R.A.F.F REST API",
    description="Interface de controle e acompanhamento pedagógico do R.A.F.F",
    version="2.0.0",
)

security = HTTPBasic()


def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Valida a senha de administrador fornecida no header HTTP Basic."""
    if not verify_admin_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha de administrador incorreta.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/status", tags=["Status"])
def read_status():
    """Retorna o status geral do estudante e da rede."""
    return {
        "estudante": STUDENT_NAME,
        "responsavel": TEACHER_NAME,
        "rede_bloqueada": get_network_state(),
        "total_questoes_locais": len(get_local_questions()),
        "status": "online"
    }


@app.get("/questoes", tags=["Questões"])
def list_questions(admin: str = Depends(get_current_admin)):
    """Lista todas as questões cadastradas localmente."""
    return get_local_questions()


@app.post("/questoes", tags=["Questões"])
def create_question(question: Dict[str, Any], admin: str = Depends(get_current_admin)):
    """Adiciona uma nova questão ao banco local."""
    if "pergunta" not in question or "opcoes" not in question:
        raise HTTPException(status_code=400, detail="Formato inválido para questão.")
    add_local_question(question)
    return {"message": "Questão adicionada com sucesso!"}


@app.get("/estatisticas", tags=["Estatísticas"])
def read_stats(admin: str = Depends(get_current_admin)):
    """Retorna o histórico de progresso e estatísticas de foco."""
    return get_stats()


@app.get("/feedbacks", tags=["Feedbacks"])
def list_feedbacks(admin: str = Depends(get_current_admin)):
    """Retorna os feedbacks pedagógicos registrados."""
    return get_feedbacks()


@app.post("/feedbacks", tags=["Feedbacks"])
def create_feedback(data: Dict[str, str], admin: str = Depends(get_current_admin)):
    """Adiciona uma nova observação pedagógica."""
    texto = data.get("texto", "").strip()
    if not texto:
        raise HTTPException(status_code=400, detail="O texto do feedback não pode ser vazio.")
    add_feedback(texto)
    return {"message": "Feedback pedagógico registrado com sucesso!"}


@app.post("/controle/liberar-rede", tags=["Controle"])
def unblock_network(admin: str = Depends(get_current_admin)):
    """Desbloqueia a rede manualmente."""
    enable_network()
    return {"message": "Rede liberada com sucesso."}


@app.post("/controle/bloquear-rede", tags=["Controle"])
def block_network(admin: str = Depends(get_current_admin)):
    """Bloqueia a rede para iniciar foco imediato."""
    disable_network()
    return {"message": "Rede bloqueada com sucesso."}


def run_server():
    """Inicia o servidor REST FastAPI."""
    uvicorn.run(app, host=API_HOST, port=API_PORT)


if __name__ == "__main__":
    run_server()
