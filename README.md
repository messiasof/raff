# 🧠 R.A.F.F
*Que significa: Rotina de Aprendizado Focada e Flexível.*

Uma ferramenta simples, pensada e feita com carinho para ajudar meu irmão Rafael e outras pessoas neurodivergentes a transformar a saída para a internet em uma recompensa por aprendizado. O objetivo não é "controlar" ninguém, e sim oferecer um fluxo de estudos previsível, supervisionado e configurável, respeitando o ambiente favorito do aluno: o computador.

---

## Por que isso importa?

Viver com autismo frequentemente implica rotinas rígidas e preferências sensoriais. Para muitas pessoas, o computador é um ambiente seguro e reiterador. A intenção é usar isso como vantagem pedagógica. Criei o R.A.F.F porque queria uma solução prática para ajudar o Rafael a:

- Se adaptar aos estudos de forma progressiva e controlada por mim, podendo adaptar as perguntas do dia ao emocional dele.

- Garantir que ele crie um hábito saudável no ambiente que ele mais gosta, o computador. De forma que não seja imponente, agressiva ou frustrante.

- Manter conteúdo apresentado de forma limpa, sem sobrecarga sensorial.

- Evitar "trapaças" simples (reiniciar/fechar o computador) graças à persistência do último conjunto de questões.

---

Esse projeto nasceu do cuidado de um irmão e de bons princípios de design para educação: previsibilidade, feedback claro, reforço positivo e personalização por parte do tutor que controla as perguntas do dia.

---

## Técnicas e princípios pedagógicos aplicados

Nem só de programação vive o dev, haha!

Um pouco de literatura pedagógica e decidi focar nos seguintes pontos durante a concepção dessa solução, traduzido a educação no que eu faço de melhor: **Criar coisas.**

- **Reforço positivo**: acesso restaurado + mensagem de parabéns ao completar.

- **Previsibilidade e rotina**: comportamento determinístico. Se as respostas estiverem corretas, a consequência é conhecida.

- **Minimização de sobrecarga sensorial**: interface limpa em PyQt6, sem animações ou sons intrusivos — mas com sons comemorativos opcionais e personalizáveis pelo próprio estudante.

- **Supervisão e consentimento**: projetado para ser usado com acompanhamento quando apropriado; configurações críticas exigem senha do responsável e ficam criptografadas.

- **Fallback resiliente**: persistência local para evitar perda de conteúdo e reduzir frustração — inclusive quando a IA ou a internet ficam indisponíveis.

---

## Principais características

- **System Tray Permanente**: roda na bandeja do Windows em segundo plano, sem precisar do Task Scheduler. Inicia com o sistema operacional.
- **Banco Local de Questões (Offline)**: o responsável cadastra perguntas e explicações pela interface gráfica. Funciona sem internet.
- **Inteligência Artificial (Google Gemini)**: geração dinâmica de perguntas adaptadas às dificuldades e ao histórico pedagógico do estudante, com fallback automático e seguro para o banco local.
- **Aviso Prévio Suave**: notificações toast nativas no Windows X minutos antes da sessão, para o estudante salvar o jogo ou terminar o que está fazendo.
- **Painel do Responsável Protegido**: controle de matérias, horários, questões e adaptadores de rede — protegido por senha criptografada sem recuperação. O estudante não consegue modificar nada crítico.
- **Personalização pelo Estudante**: som de vitória, imagem de fundo e cor do tema — tudo configurável livremente sem precisar de senha.
- **API REST Local/LAN**: monitoramento e controle remoto pelo responsável via navegador ou aplicativo na mesma rede.
- **Instalador MSI e Versão Portátil**: instalação tradicional com atalho no menu iniciar, ou pasta `.zip` sem instalação.

---

## 🚀 Como Executar

### Requisitos
- Windows 10 ou 11 (64-bit)
- Python 3.8+ (apenas para execução a partir do código-fonte)

### Executando a partir do código-fonte

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/messias-autismhelper.git
cd messias-autismhelper

# 2. Instale as dependências
pip install -r requirements.txt
pip install -e .

# 3. Inicie o R.A.F.F
raff start
```

### Comandos disponíveis

```bash
raff start              # Inicia a aplicação com interface gráfica (padrão)
raff start --headless   # Inicia em modo terminal, sem GUI
raff gui                # Alias para raff start
raff warn "mensagem"    # Envia uma notificação de aviso
raff api                # Inicia o servidor da API REST
raff config             # Abre a janela de configurações
raff healthcheck        # Verifica a instalação
raff --version          # Exibe a versão
```

---

## 📚 Documentação

- [Guia de Instalação](docs/instalacao.md)
- [Guia de Configuração](docs/configuracao.md)
- [Guia do Estudante](docs/uso-estudante.md)
- [Guia do Responsável](docs/uso-responsavel.md)
- [Documentação da API REST](docs/api.md)
- [Guia de Desenvolvimento](docs/desenvolvimento.md)
- [Funcionalidades Legadas e Stubs](docs/stubs.md)

---

## 📄 Licença
Distribuído sob licença MIT. Feito com dedicação para apoiar famílias e educadores.
