# R.A.F.F
*Que significa: Rotina de Aprendizado Focada e Flexível.*

Uma ferramenta simples, pensada e feita com carinho para ajudar meu irmão Rafael e outras pessoas neurodivergentes a transformar a saída para a internet em uma recompensa por aprendizado. O objetivo não é “controlar” ninguém, e sim oferecer um fluxo de estudos previsível, supervisionado e configurável, respeitando o ambiente favorito do aluno: o computador.

Se você quiser pular direto para a parte de como usar, [clique nesse link.](#forma-de-usar-até-o-momento-windows)

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

- Extensível e facilmente configurável via `_config.py`.

## Técnicas e princípios pedagógicos aplicados

Nem só de programação vive o dev, haha! 

Um pouco de literatura pedagógica e decidi focar nos seguintes pontos durante a concepção dessa solução, traduzido a educação no que eu faço de melhor: **Criar coisas.**

- Reforço positivo: acesso restaurado + mensagem de parabéns ao completar.

- Previsibilidade e rotina: comportamento determinístico. Se as respostas estiverem corretas, a consequência é conhecida.

- Minimização de sobrecarga sensorial: interface textual simples, sem animações ou sons intrusivos.

- Supervisão e consentimento: projetado para ser usado com acompanhamento quando apropriado; configurações permitem ajustar rigidez e escopo.

- Fallback resiliente: persistência local para evitar perda de conteúdo e reduzir frustração.

## Como funciona — visão técnica (fluxo)

O script faz um fetch no URL de checagem (definido em `_config.py`) para verificar se está liberado executar.

Se o conteúdo coincidir com o valor esperado (também no `_config.py`), o script faz outro fetch no URL de perguntas e baixa as questões.

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
  - [x] Adicionar fallback para uso offline em caso de erros
  - [x] Adicionar tratamentos de erros
  - [x] Melhorar a estrutura do _config.py
  - [x] Adicionar comentários mais úteis e claros
  - [x] Melhorar o .gitignore
  - [ ] Aviso prévio (x horas ou minutos) antes de executar o código
  - [ ] Melhorar nome dos arquivos
  - [ ] Adicionar splashscreen ASCII-art como loading
  - [x] Finalizar README com introdução, detalhes, instruções
  - [ ] Adicionar troubleshoot e artigo científico sobre o R.A.F.F (feito por mim) junto com imagens no README.
  - [ ] Adicionar nome na janela .py (quando executado via processo, tipo `cmd` ou `taskschd`)
  - [ ] Melhorar tratamento de fechamento de janela (Windows)
  - [ ] Melhorar a configuração de adpatadores e limpar o código `net.py`
  - [ ] Se não tiver .lastcheck e .lastvalue, criar
  - [ ] Adicionar IA para otimizar estudos
  - [ ] Usar env-vars para se livrar do `_config.py`

<br>

- [ ] **Tarefas para a V2/RELEASE**
  - [ ] Criar uma versão instalável para Windows
  - [ ] Melhorar o sistema do var.txt (ou me livrar dele)
  - [ ] Implementar a versão GUI com customização de usuário (sons, imagens) usando o `.config`
  - [ ] Tirar a necessidade do uso do Task Scheduler do Windows (restart + periódico)
  - [ ] Criação de uma API
  - [ ] Criação de um website para o projeto

<br><br>

# Forma de usar até o momento (Windows)
Essa seção está em construção, a escrita é simplória.

1. Baixe o projeto

2. Entre na pasta raiz do projeto

3. Baixe as dependências com `pip install -r requirements.txt`

4. Configure o `_config.py` (eu uso pastebin no modo `Raw` na variável `URL` e `URLCHECK`)

5. Adicione uma tarefa no task scheduler do Windows e configure para ela executar o `_main.py` do projeto

6. Adicione os trigger ao seu bel-prazer: eu gosto de usar um a cada 2 horas e outro ao reiniciar o PC