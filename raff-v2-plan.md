# Plano de Implementação — R.A.F.F v2.0

## Visão Geral

Refatoração completa do R.A.F.F de uma ferramenta CLI + Task Scheduler para uma **aplicação Windows nativa e autossuficiente**, com:

- System Tray permanente que substitui o Task Scheduler
- GUI PyQt6 para configurações do estudante e do adulto responsável
- Senha de administrador criptografada (sem recuperação) protegendo funções críticas
- Questões locais cadastradas pela GUI (substitui Pastebin)
- Toast notifications para avisos prévios configuráveis
- Fallback inteligente para indisponibilidade da API Gemini
- API REST local/LAN para controle remoto pelo responsável
- Instalador MSI + versão portátil .zip
- CLI mantida para uso avançado
- Tudo em pt-BR

O scaffolding será refeito com nova estrutura de pastas. Todos os scripts existentes serão refatorados e integrados ao novo core.

---

## Estrutura de Pastas Proposta

```
raff/
├── raff/                        # Pacote principal (renomeado de src/)
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── app.py               # Orquestração do quiz (refatorado)
│   │   ├── config.py            # Configuração (refatorado)
│   │   ├── network.py           # Controle de rede (refatorado)
│   │   ├── storage.py           # Persistência (refatorado)
│   │   ├── ai_engine.py         # Gemini AI (refatorado com fallback)
│   │   ├── scheduler.py         # NOVO: scheduler interno (substitui Task Scheduler)
│   │   └── security.py          # NOVO: senha admin + criptografia
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── tray.py              # NOVO: System Tray app (PyQt6)
│   │   ├── main_window.py       # NOVO: janela principal de configurações
│   │   ├── quiz_window.py       # NOVO: janela do quiz (substitui ui.py urwid)
│   │   ├── admin_dialog.py      # NOVO: diálogo de senha admin
│   │   ├── questions_editor.py  # NOVO: editor de questões (protegido por senha)
│   │   └── assets/              # Sons e imagens padrão
│   ├── api/
│   │   ├── __init__.py
│   │   └── server.py            # NOVO: FastAPI local/LAN
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py          # Refatorado
│   └── warn.py                  # Refatorado (toast notification)
├── data/                        # Persistência em runtime (não versionado)
├── docs/                        # NOVO: documentação em pt-BR
│   ├── instalacao.md
│   ├── configuracao.md
│   ├── uso-estudante.md
│   ├── uso-responsavel.md
│   ├── api.md
│   ├── desenvolvimento.md
│   └── stubs.md                 # NOVO: explica suporte legado a URLs Pastebin
├── installer/
│   ├── build_msi.py             # NOVO: script cx_Freeze para MSI
│   └── build_portable.py        # NOVO: script PyInstaller para .zip
├── tests/                       # NOVO: testes unitários
├── README.md                    # Atualizado (sem TO-DOs)
├── requirements.txt             # Atualizado com novas dependências
├── setup.py                     # Atualizado
├── pyproject.toml               # NOVO: padrão moderno de empacotamento
└── healthcheck.py               # Refatorado
```

---

## Dependências Novas

```
PyQt6                  # GUI e System Tray
fastapi                # API REST
uvicorn                # Servidor ASGI para FastAPI
cryptography           # Criptografia de dados sensíveis (questões, senha admin)
bcrypt                 # Hash seguro da senha do administrador
win11toast             # Toast notifications nativas do Windows
pyinstaller            # Build do portátil .zip
cx_Freeze              # Build do instalador MSI
```

---

## Sub-tarefas

---

### Sub-tarefa 1 — Novo Scaffolding e Migração de Core

**Status**: `[ ] pendente`

**Intenção**  
Reorganizar a estrutura de pastas do projeto para o novo layout `raff/core/`, migrar todos os módulos existentes para os novos caminhos, atualizar imports, e estabelecer as bases do `pyproject.toml`. Nenhuma funcionalidade nova é adicionada aqui — apenas a reorganização limpa.

**Resultados Esperados**
- Estrutura de pastas conforme o layout proposto acima
- Todos os módulos existentes migrados para `raff/core/`
- `pyproject.toml` criado como padrão moderno de empacotamento
- `requirements.txt` atualizado com todas as novas dependências
- `setup.py` atualizado com novos entry points
- `healthcheck.py` refatorado para novos caminhos
- `raff start` e `raff warn` continuam funcionando após a migração
- Pasta `docs/` criada com arquivos `.md` vazios (preenchidos na sub-tarefa 12)

**Lista de Passos**
1. Criar nova estrutura de pastas: `raff/core/`, `raff/gui/`, `raff/api/`, `raff/cli/`, `docs/`, `installer/`, `tests/`
2. Mover `src/app.py` → `raff/core/app.py`, `src/config.py` → `raff/core/config.py`, etc.
3. Mover `src/cli/` → `raff/cli/`
4. Atualizar todos os imports internos (`from src.` → `from raff.`)
5. Criar `pyproject.toml` com metadados do projeto, entry points e dependências
6. Atualizar `requirements.txt` incluindo PyQt6, fastapi, uvicorn, cryptography, bcrypt, win11toast, pyinstaller, cx_Freeze
7. Atualizar `setup.py` para novos caminhos e novos entry points (`raff start`, `raff gui`, `raff warn`, `raff api`)
8. Refatorar `healthcheck.py` para novos caminhos
9. Criar `docs/` com arquivos `.md` placeholder
10. Criar `raff/gui/assets/` e copiar o arquivo `.wav` existente como som padrão

**Contexto Relevante**
- `src/` atual contém: `main.py`, `app.py`, `config.py`, `ui.py`, `network.py`, `storage.py`, `ai_engine.py`, `warn.py`, `cli/`
- `setup.py` atual define entry points para `raff start` e `raff warn`
- Imports em todos os arquivos usam `from src.` ou `from .`

---

### Sub-tarefa 2 — Módulo de Segurança (Senha Admin + Criptografia)

**Status**: `[ ] pendente`

**Intenção**  
Criar o módulo `raff/core/security.py` que gerencia a senha do administrador e a criptografia dos dados sensíveis. A senha é hasheada com bcrypt, não tem recuperação, e protege qualquer ação crítica. Questões e configurações protegidas são criptografadas em repouso com `cryptography.fernet`.

**Resultados Esperados**
- `raff/core/security.py` com funções de hash, verificação e criptografia
- Senha de admin configurada na primeira execução (não pode ser em branco)
- Mensagem clara de aviso: "Anote sua senha em local seguro — não há recuperação"
- Questões e configurações críticas criptografadas no diretório `data/`
- Função `require_admin_password(action_name)` que bloqueia ações críticas
- Sem modo de reset/recuperação de senha — by design

**Lista de Passos**
1. Criar `raff/core/security.py`
2. Implementar `hash_password(plain)` usando bcrypt
3. Implementar `verify_password(plain, hashed)` para verificação
4. Implementar `setup_admin_password(plain)` — salva hash em `data/.admin_hash`
5. Implementar `is_admin_password_set()` — verifica se já foi configurada
6. Implementar `generate_fernet_key_from_password(plain)` — deriva chave de criptografia da senha usando `PBKDF2HMAC`
7. Implementar `encrypt_data(data_str, plain_password)` e `decrypt_data(encrypted_bytes, plain_password)`
8. Implementar `require_admin_password(action_name)` — retorna `True/False` após verificação
9. Garantir que `data/.admin_hash` e `data/.fernet_salt` sejam criados na primeira configuração
10. Adicionar aviso explícito de não-recuperação em todas as UIs que chamam setup

**Contexto Relevante**
- `raff/core/storage.py` gerencia o diretório `data/` — usar a mesma convenção para novos arquivos
- A senha protege: edição de questões, alteração de horários, desativação do quiz, configurações de rede, reset de dados
- O estudante **nunca** vê nem acessa este módulo diretamente

---

### Sub-tarefa 3 — Questões Locais (Substitui Pastebin)

**Status**: `[ ] pendente`

**Intenção**  
Substituir a dependência do Pastebin por um banco de questões local criptografado, gerenciável apenas pela GUI com senha de admin. O `raff/core/app.py` passa a buscar questões localmente (ou via Gemini AI) em vez de URLs remotas. A URL remota fica como opção opcional, não obrigatória.

**Resultados Esperados**
- `raff/core/storage.py` atualizado com funções de leitura/escrita de questões locais criptografadas
- Questões armazenadas em `data/.questions.enc` (criptografado com Fernet)
- `raff/core/app.py` atualizado: prioridade = AI (se configurado) → questões locais → URL remota (opcional) → cache (fallback)
- Formato interno das questões preservado (dict com `question`, `explain`, `answer`)
- Suporte a múltiplos conjuntos de questões por matéria/dia da semana
- Nenhuma questão pode ser lida sem a senha de admin (apenas o quiz usa a chave derivada em tempo de execução)

**Lista de Passos**
1. Atualizar `raff/core/storage.py` com `save_questions_encrypted(questions_list, password)` e `load_questions_encrypted(password)`
2. Definir formato interno: JSON array de `{materia, dia_semana, question, explain, answer}`
3. Criar `raff/core/app.py` com nova lógica de prioridade de fonte de questões
4. Tornar `URL_QUESTIONS` e `URL_CHECK` opcionais no `config.py` (sem erro se ausentes)
5. Remover a dependência obrigatória de Pastebin do `.env.example`
6. Atualizar `.env.example` para refletir que URLs são opcionais
7. Garantir que o quiz funcione completamente offline com questões locais

**Contexto Relevante**
- `raff/core/security.py` (sub-tarefa 2) fornece as funções de criptografia
- `raff/core/ai_engine.py` permanece como fonte primária quando `AI_MODE=True`
- O fluxo de fallback atual já existe em `src/app.py` — apenas reordenar a prioridade

---

### Sub-tarefa 4 — Fallback Inteligente do Gemini

**Status**: `[ ] pendente`

**Intenção**  
Melhorar o tratamento de erros do `raff/core/ai_engine.py` para detectar especificamente esgotamento de créditos, quota excedida ou indisponibilidade da API, e em vez de travar o PC ou bloquear a rede, notificar o adulto responsável e pular o quiz do dia de forma graciosa.

**Resultados Esperados**
- `raff/core/ai_engine.py` com categorização de erros: `QuotaExceededError`, `NetworkUnavailableError`, `APIError`
- Quando Gemini falha por falta de crédito/quota: log do erro + notificação ao adulto + skip do quiz (sem bloquear rede)
- Quando há questões locais disponíveis: usar como fallback automático sem pular o quiz
- Quando não há nenhuma fonte de questões: skip com notificação
- O PC nunca fica travado sem internet por causa de falha da API

**Lista de Passos**
1. Criar exceções customizadas: `QuotaExceededError`, `NetworkUnavailableError`, `GeminiAPIError`
2. Atualizar `generate_questions_with_ai()` para capturar e categorizar erros da API Gemini
3. Identificar erro de quota pelos códigos HTTP 429 ou mensagens específicas da API
4. Atualizar `raff/core/app.py`: em caso de `QuotaExceededError` → tentar questões locais → se não houver → skip com notificação
5. Criar função `notify_adult_of_error(error_type, message)` — escreve em `data/.error_log.json` e exibe notificação via system tray (quando disponível)
6. Garantir que `run_quiz()` nunca chame `disable_network()` se não há questões disponíveis
7. Adicionar testes unitários básicos para os cenários de fallback

**Contexto Relevante**
- `src/ai_engine.py` atual tem try/except genérico — precisa ser mais específico
- `src/app.py` atual: `get_questions()` retorna last cached se AI falha — manter mas melhorar
- A notificação ao adulto via system tray depende da sub-tarefa 5 (scheduler/tray) — usar log como fallback inicial

---

### Sub-tarefa 5 — System Tray App (Substitui Task Scheduler)

**Status**: `[ ] pendente`

**Intenção**  
Criar o `raff/gui/tray.py` — o coração da nova arquitetura. Um processo PyQt6 que roda permanentemente na bandeja do sistema, substitui completamente o Windows Task Scheduler, agenda automaticamente o quiz e os avisos prévios, e oferece menu de contexto para acesso às configurações.

**Resultados Esperados**
- `raff/gui/tray.py` com `RaffTrayApp` que persiste na bandeja do sistema
- Ícone na bandeja com menu de contexto (pt-BR): Abrir Configurações, Executar Quiz Agora, Sobre, Sair (protegido por senha)
- Scheduler interno baseado em thread/QTimer que verifica horários configurados
- Quiz executado automaticamente nos horários configurados
- Processo registrado para iniciar com o Windows via chave de registro (`HKCU\...\Run`)
- Estudante não consegue fechar o app sem senha de admin
- "Sair" no menu de contexto pede senha de admin antes de encerrar

**Lista de Passos**
1. Criar `raff/gui/tray.py` com classe `RaffTrayApp(QSystemTrayIcon)`
2. Criar ícone SVG/PNG para o app (simples, 16x16 e 32x32) e salvar em `raff/gui/assets/`
3. Implementar menu de contexto com ações em pt-BR
4. Implementar `RaffScheduler` (QTimer-based) que verifica a cada minuto se é hora do quiz ou do aviso
5. Integrar com `raff/core/scheduler.py` para leitura dos horários configurados
6. Implementar `register_startup()` e `unregister_startup()` — modifica registro do Windows (protegido por senha admin)
7. Interceptar fechamento de janela e evento de logoff para garantir restauração de rede
8. "Sair" abre `AdminDialog` (sub-tarefa 7) antes de encerrar o processo
9. Criar `raff/core/scheduler.py` com funções para ler/salvar horários configurados em `data/.schedule.json`
10. Adicionar entry point `raff gui` no `setup.py` que inicia o tray app

**Contexto Relevante**
- `src/main.py` atual tem `prevent_close()` e `install_close_prevention()` — migrar e evoluir esta lógica
- O registro do Windows para auto-start: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- PyQt6 `QSystemTrayIcon` + `QMenu` para o tray
- A instalação via MSI (sub-tarefa 10) deve criar atalho de startup apontando para `raff gui`

---

### Sub-tarefa 6 — Toast Notifications (Aviso Prévio Configurável)

**Status**: `[ ] pendente`

**Intenção**  
Substituir o `warn.py` atual (MessageBox bloqueante) por toast notifications nativas do Windows, não-bloqueantes, configuráveis em quantidade de minutos antes do quiz. O estudante vê um aviso amigável sem que o computador trave ou o prompt bloqueie.

**Resultados Esperados**
- `raff/warn.py` refatorado usando `win11toast` ou `plyer` para toast não-bloqueante
- Aviso enviado X minutos antes do horário do quiz (configurável via GUI)
- Múltiplos avisos possíveis (ex: 30min, 15min, 5min antes) — configurável
- Fallback para `MessageBox` se `win11toast` não disponível
- `raff warn "mensagem"` CLI continua funcionando
- Aviso exibe nome do estudante e horário do próximo quiz

**Lista de Passos**
1. Atualizar `requirements.txt` com `win11toast` (Windows) / `plyer` (fallback)
2. Refatorar `raff/warn.py`: criar `show_toast(title, message, duration=10)` não-bloqueante
3. Criar `show_warning_before_quiz(minutes_before, student_name, quiz_time)` com mensagem formatada
4. Integrar com o scheduler da sub-tarefa 5: o `RaffScheduler` dispara toasts nos momentos corretos
5. Manter compatibilidade do comando CLI `raff warn "mensagem"` 
6. Adicionar campo de configuração de aviso prévio na GUI (sub-tarefa 8): lista de horários em minutos
7. Salvar configuração de avisos em `data/.schedule.json` junto com os horários do quiz

**Contexto Relevante**
- `src/warn.py` atual usa `ctypes.windll.user32.MessageBoxW` — bloqueante, precisa ser substituído
- `win11toast` usa Windows Action Center (não-bloqueante, moderno)
- O scheduler da sub-tarefa 5 chama as funções deste módulo

---

### Sub-tarefa 7 — GUI: Janela de Quiz (Substitui UI urwid)

**Status**: `[ ] pendente`

**Intenção**  
Criar `raff/gui/quiz_window.py` — uma janela PyQt6 que substitui completamente a interface urwid baseada em terminal. A janela é visual, limpa, sem distrações, mas com personalizações do estudante (sons, imagens de fundo). Não pode ser fechada durante o quiz sem senha de admin.

**Resultados Esperados**
- `raff/gui/quiz_window.py` com `QuizWindow(QMainWindow)` funcional
- Layout: área de explicação (esquerda) + área de pergunta e input (direita) — similar ao atual
- Personalizações do estudante: imagem de fundo, cor do tema, som de conclusão (configuráveis sem senha)
- Janela em fullscreen ou maximizada, sem barra de tarefas
- Botão/tecla de fechar interceptado — pede senha de admin
- Som de vitória tocado ao concluir todas as questões
- Suporte a teclado: ENTER para confirmar, sem outros atalhos de saída
- Feedback visual imediato: ✔ verde / ✖ vermelho animado

**Lista de Passos**
1. Criar `raff/gui/quiz_window.py` com `QuizWindow(QMainWindow)`
2. Implementar layout em duas colunas com `QSplitter` ou `QHBoxLayout`
3. Painel esquerdo: `QTextBrowser` para explicação (estilizado)
4. Painel direito: `QLabel` para pergunta, `QLineEdit` para resposta, `QLabel` para feedback
5. Implementar lógica de verificação de resposta (case-insensitive, mesma lógica do `ui.py` atual)
6. Interceptar `closeEvent` para pedir senha de admin via `AdminDialog`
7. Implementar `apply_student_theme(config)` — carrega cor/imagem de fundo das preferências do estudante
8. Implementar som de vitória com `QSoundEffect` ou `pygame.mixer` ao concluir
9. Remover `src/ui.py` (urwid) após validação
10. Criar `raff/gui/admin_dialog.py` com `AdminDialog(QDialog)` — campo de senha, botão confirmar, mensagem de erro

**Contexto Relevante**
- `src/ui.py` atual: `QuizUI` com urwid — replicar a lógica de verificação em `quiz_window.py`
- As preferências do estudante são salvas em `data/.student_prefs.json` (novo arquivo)
- `raff/core/app.py` chama a UI — atualizar para chamar `QuizWindow` em vez de `QuizUI`

---

### Sub-tarefa 8 — GUI: Janela de Configurações

**Status**: `[ ] pendente`

**Intenção**  
Criar `raff/gui/main_window.py` — a janela principal de configurações acessível pelo menu da bandeja. Dividida em seções: configurações do estudante (livres) e configurações do administrador (protegidas por senha). Tudo via GUI, sem editar `.env` manualmente.

**Resultados Esperados**
- `raff/gui/main_window.py` com `MainWindow(QMainWindow)` com abas
- Aba "Estudante": nome, som de vitória (upload), imagem de fundo (upload), cor do tema
- Aba "Responsável" (protegida por senha): horários do quiz, matérias por dia, chave Gemini, adaptadores de rede, aviso prévio, ativar/desativar quiz
- Aba "Questões" (protegida por senha): CRUD de questões locais por matéria
- Aba "Sobre": versão, créditos, link do projeto
- Configurações salvas em `data/.config.json` (geral) e `data/.config.enc` (dados sensíveis criptografados)
- Primeiro uso: wizard de configuração inicial (setup da senha admin + configurações básicas)

**Lista de Passos**
1. Criar `raff/gui/main_window.py` com `MainWindow(QMainWindow)`
2. Implementar sistema de abas com `QTabWidget`
3. Aba "Meu Perfil" (estudante): campos para nome, upload de som (.wav/.mp3), upload de imagem de fundo
4. Aba "Responsável": campos de horários (QTimeEdit), matérias por dia (QComboBox), avisos prévios (lista de minutos), toggle ativo/inativo
5. Aba "Questões": `QuestionsEditor` (sub-item) com tabela CRUD de questões por matéria
6. Implementar proteção por senha: ao clicar em aba protegida → abre `AdminDialog` → se correto, desbloqueia temporariamente
7. Criar wizard de primeiro uso: `FirstRunWizard(QWizard)` — cria senha admin + configura nome + configura primeira matéria
8. Implementar `save_config()` e `load_config()` — salva partes livres em `.config.json`, partes sensíveis em `.config.enc`
9. Criar `raff/gui/questions_editor.py` com `QuestionsEditor(QWidget)` — tabela editável de questões
10. Substituir totalmente o uso de `.env` por este sistema de configuração (`.env` fica somente para desenvolvimento)

**Contexto Relevante**
- `raff/core/config.py` atual lê `.env` — será substituído/complementado por leitura do `data/.config.json`
- `raff/core/security.py` (sub-tarefa 2) fornece encrypt/decrypt para a aba do responsável
- `raff/gui/admin_dialog.py` (sub-tarefa 7) é reutilizado aqui para proteção das abas

---

### Sub-tarefa 9 — API REST (FastAPI local/LAN)

**Status**: `[ ] pendente`

**Intenção**
Criar `raff/api/server.py` — uma API FastAPI leve que roda localmente (ou na LAN) e permite ao adulto responsável gerenciar o app remotamente: ver status, adicionar questões, alterar horários, ver logs de sessão.

**Resultados Esperados**
- `raff/api/server.py` com FastAPI app funcional
- Endpoints protegidos por autenticação (senha de admin via HTTP Basic + `security.verify_password()`)
- Endpoints: `GET /status`, `GET /questoes`, `POST /questoes`, `GET /agenda`, `PUT /agenda`, `GET /logs`, `POST /quiz/executar-agora`
- Host padrão: `127.0.0.1` (localhost apenas) — opção mais segura; responsável pode habilitar `0.0.0.0` para LAN explicitamente via GUI
- Porta padrão: `8472` (configurável)
- Inicia como thread daemon no processo do system tray quando habilitado
- Documentação Swagger em `/docs` (pt-BR)
- `raff api` como comando CLI para iniciar standalone se necessário

**Lista de Passos**
1. Criar `raff/api/server.py` com `app = FastAPI(title="R.A.F.F API", ...)`
2. Implementar autenticação: `HTTPBasic` com verificação via `security.verify_password()`
3. Implementar `GET /status` — retorna estado atual: quiz ativo, próximo horário, questões carregadas
4. Implementar `GET/POST /questoes` — lista e adiciona questões (descriptografa/criptografa com senha do admin)
5. Implementar `GET/PUT /agenda` — lê e altera horários
6. Implementar `GET /logs` — retorna últimas sessões de `data/.session_log.json`
7. Implementar `POST /quiz/executar-agora` — dispara quiz imediatamente
8. Integrar inicialização da API no system tray (sub-tarefa 5): thread daemon com uvicorn, bind em `127.0.0.1` por padrão
9. Adicionar configuração de porta e toggle "Expor na LAN" na aba Responsável da GUI (sub-tarefa 8); habilitar LAN requer senha admin
10. Adicionar entry point `raff api` no `setup.py`

**Contexto Relevante**
- FastAPI + uvicorn rodam em thread separada, sem bloquear o event loop do Qt
- A autenticação reutiliza `raff/core/security.py` — sem senha separada para a API
- Logs de sessão serão criados em `raff/core/app.py` ao final de cada quiz

---

### Sub-tarefa 10 — Instalador MSI + Versão Portátil

**Status**: `[ ] pendente`

**Intenção**  
Criar os scripts de build para gerar duas distribuições: um instalador MSI para instalação tradicional no Windows (com atalho no menu iniciar e opção de iniciar com o Windows) e uma versão portátil como pasta .zip com executável único gerado pelo PyInstaller.

**Resultados Esperados**
- `installer/build_msi.py` gerando `raff-setup.msi` via cx_Freeze
- `installer/build_portable.py` gerando `raff-portable.zip` via PyInstaller
- MSI: instala em `C:\Program Files\RAFF\`, cria atalho no menu iniciar, opção de iniciar com Windows
- Portátil: pasta autocontida, rodar `raff.exe` inicia o system tray
- Ambos incluem todos os assets (ícone, sons padrão)
- Instruções de build documentadas em `docs/desenvolvimento.md`

**Lista de Passos**
1. Criar `installer/build_msi.py` com configuração do cx_Freeze: `executables`, `options`, `include_files`
2. Configurar cx_Freeze para incluir PyQt6, FastAPI, cryptography e dependências
3. Criar `installer/build_portable.py` com spec do PyInstaller: `--onefile` ou `--onedir`, `--windowed`, `--icon`
4. Configurar PyInstaller para empacotar assets (`raff/gui/assets/`)
5. Adicionar script `installer/create_release.py` que chama ambos e cria pasta `dist/`
6. Documentar processo de build em `docs/desenvolvimento.md`
7. Criar arquivo `.github/workflows/build.yml` (opcional) para CI build automático

**Contexto Relevante**
- cx_Freeze gera MSI nativamente no Windows
- PyInstaller com `--onedir` é mais confiável com PyQt6 do que `--onefile`
- Incluir `vcredist` ou garantir que cx_Freeze inclua runtime necessário

---

### Sub-tarefa 11 — Refatoração da CLI

**Status**: `[ ] pendente`

**Intenção**  
Refatorar `raff/cli/commands.py` para refletir todos os novos comandos, melhorar as mensagens de ajuda em pt-BR, e garantir que a CLI continua funcional para uso avançado e debug, inclusive iniciando o quiz em modo headless (sem GUI).

**Resultados Esperados**
- `raff/cli/commands.py` atualizado com todos os comandos
- `raff start` — inicia o system tray + quiz por padrão (modo Qt); `raff start --headless` para modo CLI urwid (retrocompatibilidade)
- `raff gui` — alias explícito para iniciar o system tray app com GUI
- `raff warn "mensagem"` — exibe toast notification
- `raff api` — inicia o servidor API standalone
- `raff config` — abre a janela de configurações
- `raff healthcheck` — valida instalação
- Todas as mensagens de ajuda em pt-BR
- `--version` retorna versão atual

**Lista de Passos**
1. Refatorar `raff/cli/commands.py` com `argparse` e subcomandos
2. Subcomando `start`: padrão Qt; adicionar flag `--headless` que usa o modo urwid legado (`raff/core/app.py` + `raff/gui/headless_ui.py`)
3. Adicionar subcomando `gui` que chama `raff/gui/tray.py` (alias de `start` sem `--headless`)
4. Adicionar subcomando `api` que chama `raff/api/server.py`
5. Adicionar subcomando `config` que abre `raff/gui/main_window.py`
6. Adicionar subcomando `healthcheck` que chama `healthcheck.py` refatorado
7. Traduzir todas as strings de ajuda para pt-BR
8. Adicionar `--version` com versão do `pyproject.toml`
9. Atualizar `setup.py` entry points para todos os novos comandos

**Contexto Relevante**
- `src/cli/commands.py` atual tem apenas `start`, `test`, `warn`
- O entry point principal `raff` deve default para `raff gui` quando chamado sem argumentos

---

### Sub-tarefa 12 — Documentação em pt-BR

**Status**: `[ ] pendente`

**Intenção**
Escrever documentação completa em português brasileiro no diretório `docs/`, cobrindo instalação, configuração, uso diário do estudante, uso do responsável, referência da API, guia de desenvolvimento e um documento de stubs explicando funcionalidades legadas.

**Resultados Esperados**
- `docs/instalacao.md` — passo a passo de instalação (MSI e portátil)
- `docs/configuracao.md` — guia completo de configuração via GUI
- `docs/uso-estudante.md` — guia para o estudante (simples, visual)
- `docs/uso-responsavel.md` — guia para o adulto responsável
- `docs/api.md` — referência dos endpoints da API REST
- `docs/desenvolvimento.md` — guia para desenvolvedores (setup, build, contribuição)
- `docs/stubs.md` — explica o suporte legado a URLs Pastebin e modo `--headless`

**Lista de Passos**
1. Escrever `docs/instalacao.md` cobrindo instalador MSI e versão portátil
2. Escrever `docs/configuracao.md` com screenshots descritivos (em texto, sem imagens) de cada aba da GUI
3. Escrever `docs/uso-estudante.md` em linguagem simples e clara
4. Escrever `docs/uso-responsavel.md` cobrindo senha admin, questões, horários, API
5. Escrever `docs/api.md` com todos os endpoints, parâmetros e exemplos
6. Escrever `docs/desenvolvimento.md` com setup de dev, como fazer build, estrutura do código
7. Escrever `docs/stubs.md` explicando: (a) suporte opcional a `URL_QUESTIONS`/`URL_CHECK` via Pastebin como fonte legada de questões, (b) o flag `--headless` e quando usá-lo, (c) o arquivo `.env` como alternativa de configuração para ambientes de desenvolvimento

**Contexto Relevante**
- Todo conteúdo deve ser em pt-BR
- Não usar jargão técnico nos docs do estudante e responsável
- `docs/api.md` pode referenciar o Swagger em `/docs` do FastAPI

---

### Sub-tarefa 13 — Atualização do README

**Status**: `[ ] pendente`

**Intenção**  
Atualizar o README.md para refletir a versão 2.0 do projeto: nova arquitetura, instalação simplificada, recursos da GUI, sem seção de TO-DOs. Manter o cabeçalho atual (acima de `## Principais características`) intacto.

**Resultados Esperados**
- README.md atualizado com instrução de instalação via MSI ou portátil
- Seção "Principais características" refletindo v2.0: GUI, system tray, sem Task Scheduler
- Sem seções TO-DO (todos concluídos)
- Links para `docs/` para detalhes
- Badge de versão atualizado para v2.0

**Lista de Passos**
1. Ler o README atual — preservar tudo acima de `## Principais características`
2. Reescrever `## Principais características` listando features da v2.0
3. Reescrever seção de instalação: MSI (recomendado) e portátil
4. Reescrever seção de uso: comandos CLI atualizados + menção à GUI
5. Adicionar seção "Documentação" com links para `docs/`
6. Remover todas as seções de TO-DO e V1/V2 roadmap
7. Atualizar versão para 2.0.0

**Contexto Relevante**
- README atual começa com texto emocional/contextual sobre autismo — manter intacto
- A seção `## Principais características` é o ponto de corte para edições

---

## Ordem de Implementação

```
Sub-tarefa 1  →  Sub-tarefa 2  →  Sub-tarefa 3  →  Sub-tarefa 4
                                                        ↓
Sub-tarefa 5  ←────────────────────────────────────────┘
     ↓
Sub-tarefa 6  →  Sub-tarefa 7  →  Sub-tarefa 8
                                       ↓
Sub-tarefa 9  ←────────────────────────┘
     ↓
Sub-tarefa 10  →  Sub-tarefa 11  →  Sub-tarefa 12  →  Sub-tarefa 13
```

As sub-tarefas 1–4 são fundação (core). As sub-tarefas 5–9 são GUI/UX. As sub-tarefas 10–13 são empacotamento e documentação.

---

## Notas de Implementação

- **Idioma**: Toda string visível ao usuário em pt-BR. Nomes de variáveis e código em inglês.
- **Sem recuperação de senha**: By design. O aviso deve ser claro e repetido na GUI.
- **Sem Task Scheduler**: O instalador MSI remove qualquer instrução de Task Scheduler. O system tray cuida disso.
- **Estudante não fecha o app**: `closeEvent` interceptado em todas as janelas. Processo do tray resiste ao fechamento.
- **Portátil vs Instalável**: Ambos devem funcionar identicamente. O portátil salva `data/` na mesma pasta do executável.
- **Retrocompatibilidade CLI**: `raff start --headless` mantém o modo urwid original para usuários avançados/debug. Sem o flag, inicia o sistema Qt.
- **Segurança da API**: Host padrão é `127.0.0.1`. Expor na LAN (`0.0.0.0`) requer senha admin e é opt-in explícito.
- **Pastebin como stub legado**: `URL_QUESTIONS` e `URL_CHECK` continuam suportados como fonte opcional de questões, documentados em `docs/stubs.md`. Não são obrigatórios nem recomendados para novas instalações.
