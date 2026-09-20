# Funcionalidades Legadas e Stubs

Este documento descreve funcionalidades que existiam na v1.x do R.A.F.F e foram mantidas por retrocompatibilidade na v2.0, mas não são mais o modo recomendado de uso.

---

## 1. URLs Pastebin — Fonte Remota de Questões

Nas versões anteriores (v1.x), o R.A.F.F buscava perguntas de URLs públicas no Pastebin usando o formato de texto simples:

```
QUESTION=Quanto é 2+2?; EXPLAIN=Operação básica de soma; ANSWER=4;
QUESTION=Qual a capital do Brasil?; EXPLAIN=a) Rio b) SP c) Brasília; ANSWER=c;
```

### Variáveis de configuração legadas (`.env`):

| Variável | Descrição |
|---|---|
| `URL_QUESTIONS` | URL raw do Pastebin com as questões |
| `URL_CHECK` | URL raw de controle (se contiver `CHECK_CHAR`, o quiz executa) |
| `CHECK_CHAR` | Caractere esperado na URL de controle (ex: `1`) |

### Status na v2.0:
- As variáveis ainda são lidas do `.env` se presentes
- A prioridade de fonte de questões é: **Gemini AI → Banco Local → URL Remota → Cache**
- O Pastebin é ativado automaticamente se `URL_QUESTIONS` estiver configurado
- **Não é recomendado para novas instalações** — use o Banco Local via GUI

---

## 2. Modo Headless (`--headless`)

O comando `raff start` por padrão abre a interface gráfica Qt com ícone na bandeja.

Para compatibilidade com ambientes sem display gráfico ou para debugging via terminal, use:

```bash
raff start --headless
```

### Comportamento no modo headless:
- Abre o quiz diretamente no terminal usando a biblioteca `urwid`
- Não requer PyQt6
- Layout em duas colunas (explicação + pergunta) com cores ANSI
- Resposta via teclado — ENTER para confirmar, Q para sair
- Útil em servidores, scripts automatizados ou recuperação de emergência

### Quando usar:
- Debug de questões sem abrir a GUI
- Ambientes sem suporte a janelas gráficas
- Testes automatizados headless (CI/CD)

---

## 3. Arquivo `.env` como Configuração

Na v1.x, toda a configuração era feita editando manualmente o arquivo `.env`.

Na v2.0, a configuração é feita pela **interface gráfica** (aba Responsável, com senha). O arquivo `.env` ainda é suportado para:

- Ambientes de desenvolvimento
- Configuração inicial sem GUI disponível
- Sobreposição de variáveis em deploys automatizados

O arquivo `.env.example` na raiz do projeto documenta todas as variáveis disponíveis.

> **Nota**: Em instalações normais via MSI ou portátil, o `.env` não é necessário. A GUI persiste as configurações em `data/settings.json`.

---

## 4. Remoção do Windows Task Scheduler

Versões anteriores dependiam do **Agendador de Tarefas do Windows** para executar o R.A.F.F periodicamente.

Na v2.0 isso foi substituído pelo **scheduler interno** (`raff/core/scheduler.py`) que:
- Roda como thread dentro do processo do system tray
- Não requer configuração manual no Windows
- É configurável pela GUI (aba Responsável → horários)
- Persiste os horários em `data/settings.json`

Se você tinha tarefas agendadas da v1.x, pode removê-las com segurança após instalar a v2.0.
