# R.A.F.F
*Que significa: Rotina de Aprendizado Focada e Flexível.*

Uma ferramenta simples, pensada e feita com carinho para ajudar meu irmão Rafael e outras pessoas neurodivergentes a transformar a saída para a internet em uma recompensa por aprendizado. O objetivo não é “controlar” ninguém, e sim oferecer um fluxo de estudos previsível, supervisionado e configurável, respeitando o ambiente favorito do aluno: o computador.

## Resumo técnico 
Script Python que busca perguntas em um URL remoto, apresenta-as numa interface CLI minimalista (feito com urwid), bloqueia adaptadores de rede até as perguntas serem respondidas corretamente e persiste um fallback local para evitar perda de conteúdo caso a internet (ou o script) caia.

## Por que isso importa?

Viver com autismo frequentemente implica rotinas rígidas e preferências sensoriais. Para muitas pessoas, o computador é um ambiente seguro e reiterador. A intenção é usar isso como vantagem pedagógica. Criei o R.A.F.F porque queria uma solução prática para ajudar o Rafael a:

- Se adaptar aos estudos de forma progressiva e controlada por mim, podendo adpatar as perguntas do dia ao emocional dele.

- Garantir que ele crie um hábito saúdavel no ambiente que ele mais gosta, o computador. De forma que não seja imponente, agressiva ou frustrante.

- Manter conteúdo apresentado de forma limpa, sem sobrecarga sensorial;

- Evitar “trapaças” simples (reiniciar/fechar o computador) graças a persistência do último conjunto de questões.

---

Esse projeto nasceu do cuidado de um irmão e de bons princípios de design para educação: previsibilidade, feedback claro, reforço positivo e personalização (por parte do tutor que controla as perguntas do dia remotamente)

## Principais características

- Fetch de controle e de conteúdo a partir de URLs configuráveis.

- Formato simples de perguntas (QUESTION, EXPLAIN, ANSWER) em texto “raw”.

- Interface CLI acessível e de baixa distração construída com urwid.

- Bloqueio/reativação de adaptadores de rede configurável por sistema.

- Persistência local de fallback em `.lastvalue `(perguntas) e `.lastcheck` (último estado do controle).

- Extensível e facilmente configurável via `.env`.

## Técnicas e princípios pedagógicos aplicados

Nem só de programação vive o dev, haha! 

Um pouco de literatura pedagógica e decidi focar nos seguintes pontos durante a concepção dessa solução, traduzido a educação no que eu faço de melhor: **Criar coisas.**

- Reforço positivo: acesso restaurado + mensagem de parabéns ao completar.

- Previsibilidade e rotina: comportamento determinístico. Se as respostas estiverem corretas, a consequência é conhecida.

- Minimização de sobrecarga sensorial: interface textual simples, sem animações ou sons intrusivos.

- Supervisão e consentimento: projetado para ser usado com acompanhamento quando apropriado; configurações permitem ajustar rigidez e escopo.

- Fallback resiliente: persistência local para evitar perda de conteúdo e reduzir frustração.

## Como funciona — visão técnica (fluxo)

O script faz um fetch no URL de checagem (definido em `.env`) para verificar se está liberado executar.

Se o conteúdo coincidir com o valor esperado (também no `.env`), o script faz outro fetch no URL de perguntas e baixa as questões.

Tanto o conteúdo da checagem quanto das perguntas são guardados localmente:

`.lastcheck` é o último valor da checagem

`.lastvalue` é o último arquivo de perguntas
Isso permite exibir perguntas mesmo com internet offline caso o processo seja interrompido.

O script desabilita os adaptadores de rede configurados (não necessariamente todos) para garantir que a internet só volte ao término do exercício.

Após isso, apresenta a interface CLI com `urwid`, que mostra pergunta + texto explicativo e entrada para resposta.

Ao responder todas corretamente (comparação simples com ANSWER), o script reativa os adaptadores de rede e exibe uma mensagem de parabéns.

## Formato das perguntas (arquivo remoto)

Cada linha representa uma pergunta com três campos separados por ponto-e-vírgula ; (padrão simples). Exemplo:

```plaintext
QUESTION=Qual é a capital do Brasil?; EXPLAIN=Escolha a cidade capital; ANSWER=Brasília;
QUESTION=2+2; EXPLAIN=Operação de soma simples; ANSWER=4;
```

### Regras:

- Use `QUESTION=;` `EXPLAIN=;` e `ANSWER=;` exatamente assim.

- EXPLAIN pode ser alternativas (A/B/C) ou contexto adicional.

- Cada linha é uma pergunta independente.

- Use `\n` no `EXPLAIN=;` para pular linhas.

---

# Lista de tarefas (to-do)
- [ ] **Tarefas ainda para a V1/MVP** (essa)
  - [ ] Atualizar e melhorar o README para a última refatoração + CLI
  - [x] Adicionar fallback para uso offline em caso de erros
  - [x] Adicionar tratamentos de erros
  - [x] Melhorar a estrutura do _config.py
  - [x] Adicionar comentários mais úteis e claros
  - [x] Melhorar o .gitignore
  - [ ] Aviso prévio (x horas ou minutos) antes de executar o código
  - [x] Melhorar nome dos arquivos
  - [ ] Adicionar splashscreen ASCII-art como loading
  - [x] Finalizar README com introdução, detalhes, instruções
  - [ ] Adicionar troubleshoot e artigo científico sobre o R.A.F.F (feito por mim) junto com imagens no README
  - [ ] Adicionar nome na janela .py (quando executado via processo, tipo `cmd` ou `taskschd`)
  - [x] Melhorar tratamento de fechamento de janela (Windows)
  - [x] Melhorar a configuração de adaptadores e limpar o código `net.py`
  - [x] Se não tiver .lastcheck e .lastvalue, criar automaticamente
  - [x] Adicionar IA para otimizar estudos
  - [x] Usar env-vars para se livrar do `_config.py`
  - [x] Sistema de acumulação de feedbacks (últimos X feedbacks)
  - [x] Refatoração completa da estrutura do projeto
  - [x] Correção do problema de repetição de perguntas
  - [ ] Preparar fallback para esgotamento de créditos da IA (Gemini) e não deixar o PC travado sem internet

<br>

- [ ] **Tarefas para a V2/RELEASE**
  - [ ] Criar uma versão instalável para Windows
  - [x] Melhorar o sistema do var.txt (removido, agora usa .network_state)
  - [ ] Implementar a versão GUI com customização de usuário (sons, imagens)
  - [ ] Tirar a necessidade do uso do Task Scheduler do Windows (restart + periódico)
  - [ ] Criação de uma API
  - [ ] Criação de um website para o projeto

<br><br>

# Forma de usar até o momento (Windows)

## Instalação

1. Baixe o projeto

2. Entre na pasta raiz do projeto

3. Instale as dependências:

Se você quiser usar comandos de CLI como `raff start`, então:
```bash
pip install .
```

Mas se você só quiser as dependências pra rodar, então:
```bash
pip install -r requirements.txt
```

Não existe problema em executar ambos comandos. As dependências dos dois são sincronizadas automaticamente.

4. Configure o arquivo `.env`:
   - Copie o arquivo `.env.example` para `.env`
   - Edite o `.env` e preencha suas configurações:
     - `URL_QUESTIONS`: URL onde estão as perguntas (ex: Pastebin no modo Raw)
     - `URL_CHECK`: URL para verificar se deve executar
     - `CHECK_CHAR`: Caractere que indica execução (ex: "1")
     - `GEMINI_API_KEY`: Sua chave da API do Gemini
     - `STUDENT_NAME`: Nome do estudante
     - `TEACHER_NAME`: Nome do responsável
     - `NETWORK_DEVICE_1` e `NETWORK_DEVICE_2`: Nomes dos adaptadores de rede (veja com `netsh interface show interface`)
     - Configure as matérias por dia da semana (Segunda=0, Domingo=6)
     - `AI_MODE`: True para usar IA, False para usar perguntas remotas
     - `AI_QUESTIONS_COUNT`: Quantidade de perguntas a serem geradas
     - `MAX_FEEDBACKS`: Quantidade de feedbacks a armazenar

5. **Teste a instalação:**
   ```bash
   python healthcheck.py
   ```
   Este script verifica se tudo está configurado corretamente.

6. Adicione uma tarefa no Task Scheduler do Windows:
   - Configurar para executar: `python -m src.main`
   - Diretório inicial: pasta raiz do projeto
   - Executar com privilégios de administrador (necessário para controlar adaptadores de rede)

7. Configure os triggers conforme sua necessidade:
   - Exemplo: A cada 2 horas durante período de estudos
   - Exemplo: Sempre às 16h00 em dias normais
   - Exemplo: Ao reiniciar o PC