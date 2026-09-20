# Guia de Desenvolvimento — R.A.F.F

## Estrutura do Projeto

```
raff/
├── raff/
│   ├── core/           # Lógica de negócios (config, rede, segurança, IA, agendador)
│   ├── gui/            # Interface gráfica PyQt6 (tray, quiz, configurações)
│   ├── api/            # API REST (FastAPI + Uvicorn)
│   └── cli/            # Comandos de linha de comando
├── docs/               # Documentação em pt-BR
├── installer/          # Scripts de build (MSI e portátil)
├── tests/              # Testes unitários
├── data/               # Dados em runtime (não versionado)
└── raff-v2-plan.md     # Plano de implementação da v2.0
```

## Setup do Ambiente de Desenvolvimento

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/messias-autismhelper.git
cd messias-autismhelper

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instale as dependências (incluindo ferramentas de dev)
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Executando os Testes

```bash
# Rodar todos os testes
pytest

# Com verbose
pytest -v

# Apenas um arquivo
pytest tests/test_core.py
```

## Verificação de Integridade

```bash
python healthcheck.py
```

## Comandos CLI Disponíveis

| Comando | Descrição |
|---|---|
| `raff start` | Inicia o system tray (GUI) |
| `raff start --headless` | Inicia o quiz em modo terminal (urwid) |
| `raff gui` | Alias para `raff start` |
| `raff warn "mensagem"` | Envia uma toast notification |
| `raff api` | Inicia o servidor REST standalone |
| `raff config` | Abre a janela de configurações |
| `raff healthcheck` | Verifica a instalação |
| `raff --version` | Exibe a versão |

## Build do Instalador MSI

```bash
cd installer
python build_msi.py bdist_msi
# Saída em: dist/RAFF-2.0.0-win64.msi
```

**Pré-requisito:** `pip install cx_Freeze`

## Build da Versão Portátil

```bash
cd installer
python build_portable.py
# Saída em: dist/RAFF-Portavel/
```

**Pré-requisito:** `pip install pyinstaller`

## Módulos Principais

### `raff/core/security.py`
Gerencia a senha do administrador (bcrypt) e criptografia de dados sensíveis (Fernet/PBKDF2). Sem mecanismo de recuperação — by design.

### `raff/core/scheduler.py`
Agendador interno em thread. Substitui o Windows Task Scheduler. Verifica horários configurados a cada 30s e dispara callbacks de aviso e quiz.

### `raff/core/ai_engine.py`
Integração com Google Gemini. Fallback automático para banco local → cache → banco de emergência quando a API estiver indisponível.

### `raff/gui/tray.py`
Ponto de entrada principal da aplicação. Cria o ícone na bandeja do sistema, inicializa o scheduler e gerencia o ciclo de vida do app.

### `raff/api/server.py`
FastAPI rodando em thread daemon (porta 8765, bind em 127.0.0.1 por padrão). Autenticação HTTP Basic com a senha do admin.

## Convenções de Código

- Strings visíveis ao usuário: **sempre em pt-BR**
- Nomes de variáveis e funções: inglês
- Docstrings: pt-BR
- Senha de admin: nunca logar, nunca serializar em texto plano
- Rede: sempre restaurar no `finally` ou `atexit`

## Legados e Retrocompatibilidade

Veja [`docs/stubs.md`](stubs.md) para detalhes sobre funcionalidades legadas (Pastebin, modo headless, `.env`).
