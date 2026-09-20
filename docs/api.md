# Documentação da API REST

O R.A.F.F possui uma API REST integrada em FastAPI para monitoramento local e gerenciamento em rede local (LAN).

---

## Endpoints Principais

### `GET /status`
Retorna o estado operacional do aplicativo.
- **Autenticação**: Nenhuma

---

### `GET /questoes`
Lista todas as questões cadastradas localmente.
- **Autenticação**: HTTP Basic (Senha do Responsável)

---

### `POST /questoes`
Cadastra uma nova questão no banco de dados local.
- **Autenticação**: HTTP Basic (Senha do Responsável)

---

### `GET /estatisticas`
Obtém métricas agregadas de acertos e tempo de resposta.
- **Autenticação**: HTTP Basic (Senha do Responsável)

---

### `POST /controle/liberar-rede` e `POST /controle/bloquear-rede`
Permite o controle remoto dos adaptadores de rede.
- **Autenticação**: HTTP Basic (Senha do Responsável)
