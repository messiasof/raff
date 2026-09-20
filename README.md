# 🧠 R.A.F.F — Rotina de Aprendizado e Foco Familiar

<p align="center">
  <b>Aplicação Windows nativa para suporte e rotina de foco no aprendizado</b><br>
  Construída especialmente para estudantes neurodivergentes e no espectro autista.
</p>

---

## 🎯 Sobre o Projeto

Criar uma rotina de estudos consistente para pessoas autistas exige paciência, previsibilidade e estratégias claras. Muitas vezes, a transição abrupta entre momentos de lazer (como jogos ou vídeos) e momentos de foco pode gerar sobrecarga sensorial e frustração.

O **R.A.F.F** foi desenvolvido para transformar esse processo em algo **previsível, amigável e comemorativo**:
- 🔔 **Aviso Prévio Suave**: Notificações toast nativas no Windows avisam antes da atividade começar para permitir que o estudante salve seus jogos ou trabalhos.
- 🔒 **Foco com Segurança**: Gestão temporária da rede durante a sessão para evitar distrações.
- 🧩 **Quiz Acessível e Adaptativo**: Interface limpa em PyQt6, com explicação pedagógica detalhada e celebrações sonoras personalizáveis.
- 🛡️ **Painel do Responsável Protegido**: Controle de matérias, horários e banco de questões protegido por criptografia e senha de administrador.

---

## ✨ Funcionalidades da Versão 2.0

- **System Tray Permanente**: Roda na bandeja do Windows em segundo plano, sem necessidade de agendadores externos.
- **Banco Local de Questões (Offline)**: Cadastro completo de perguntas e explicações via interface gráfica.
- **Inteligência Artificial (Google Gemini)**: Geração dinâmica de perguntas adaptadas às dificuldades e histórico pedagógico (com fallback automático e seguro).
- **Notificações Toast Modernas**: Alertas visuais e sonoros integrados ao Windows 10/11.
- **API REST Local/LAN**: Monitoramento e controle remoto por responsáveis conectados à mesma rede.
- **Instalador MSI e Versão Portátil**: Facilidade de instalação e início automático com o sistema.

---

## 🚀 Como Executar

### 1. Requisitos
- Windows 10 ou 11 (64-bit)
- Python 3.8+ (caso execute a partir do código-fonte)

### 2. Executando o R.A.F.F
```bash
# Iniciar a aplicação na bandeja do sistema
raff gui

# Ou iniciar diretamente uma sessão de quiz
raff start
```

---

## 📚 Documentação

- [Guia de Instalação](docs/instalacao.md)
- [Guia de Configuração](docs/configuracao.md)
- [Guia do Estudante](docs/uso-estudante.md)
- [Guia do Responsável](docs/uso-responsavel.md)
- [Documentação da API REST](docs/api.md)
- [Guia de Desenvolvimento](docs/desenvolvimento.md)

---

## 📄 Licença
Distribuído sob licença MIT. Feito com dedicação para apoiar famílias e educadores.
