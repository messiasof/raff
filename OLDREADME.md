# R.A.F.F
*Que significa: Rotina de Aprendizado Focada e Flexível.*

Uma ferramenta simples, pensada e feita com carinho para ajudar meu irmão Rafael e outras pessoas neurodivergentes a transformar a saída para a internet em uma recompensa por aprendizado. O objetivo não é “controlar” ninguém, e sim oferecer um fluxo de estudos previsível, supervisionado e configurável, respeitando o ambiente favorito do aluno: o computador.

## Resumo técnico 
Script Python que busca perguntas em um URL remoto, apresenta-as numa interface CLI minimalista (feito com urwid), bloqueia adaptadores de rede até as perguntas serem respondidas corretamente e persiste um fallback local para evitar perda de conteúdo caso a internet (ou o script) caia.
Antes de iniciar a atividade, o app pode exibir um aviso nativo do Windows configurável no `.env`. Ao terminar, ele também pode tocar um som opcional e tenta restaurar a rede automaticamente se o processo for encerrado.

## Por que isso importa?

Viver com autismo frequentemente implica rotinas rígidas e preferências sensoriais. Para muitas pessoas, o computador é um ambiente seguro e reiterador. A intenção é usar isso como vantagem pedagógica. Criei o R.A.F.F porque queria uma solução prática para ajudar o Rafael a:

- Se adaptar aos estudos de forma progressiva e controlada por mim, podendo adpatar as perguntas do dia ao emocional dele.

- Garantir que ele crie um hábito saúdavel no ambiente que ele mais gosta, o computador. De forma que não seja imponente, agressiva ou frustrante.

- Manter conteúdo apresentado de forma limpa, sem sobrecarga sensorial;

- Evitar “trapaças” simples (reiniciar/fechar o computador) graças a persistência do último conjunto de questões.

---

Esse projeto nasceu do cuidado de um irmão e de bons princípios de design para educação: previsibilidade, feedback claro, reforço positivo e personalização (por parte do tutor que controla as perguntas do dia remotamente)

## Técnicas e princípios pedagógicos aplicados

Nem só de programação vive o dev, haha! 

Um pouco de literatura pedagógica e decidi focar nos seguintes pontos durante a concepção dessa solução, traduzido a educação no que eu faço de melhor: **Criar coisas.**

- Reforço positivo: acesso restaurado + mensagem de parabéns ao completar.

- Previsibilidade e rotina: comportamento determinístico. Se as respostas estiverem corretas, a consequência é conhecida.

- Minimização de sobrecarga sensorial: interface textual simples, sem animações ou sons intrusivos.

- Supervisão e consentimento: projetado para ser usado com acompanhamento quando apropriado; configurações permitem ajustar rigidez e escopo.

- Fallback resiliente: persistência local para evitar perda de conteúdo e reduzir frustração.