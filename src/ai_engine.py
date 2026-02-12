"""
Módulo de inteligência artificial
Gerencia a geração de perguntas personalizadas usando Gemini
"""

from datetime import datetime
from google import genai

from src.config import (
    GEMINI_API_KEY,
    STUDENT_NAME,
    WEEKDAYS,
    AI_QUESTIONS_COUNT,
    MAX_FEEDBACKS,
)
from src.storage import get_feedbacks_text, add_feedback, save_last_questions


def get_current_subject() -> str:
    """Retorna a matéria do dia baseado no dia da semana."""
    weekday = datetime.today().weekday()
    return WEEKDAYS.get(weekday, "Geral")


def collect_feedback() -> str:
    """
    Coleta feedback do usuário sobre a sessão de estudos.
    
    Returns:
        Texto do feedback fornecido pelo usuário
    """
    print("\n" + "=" * 70)
    print("FEEDBACK DA SESSÃO")
    print("=" * 70)
    print("\nDiga o que você achou da sessão de estudos!")
    print("Você pode falar sobre:")
    print("  • O que aprendeu ou quer aprender")
    print("  • O que ficou confuso ou claro")
    print("  • Nível de dificuldade (fácil, médio, difícil)")
    print("  • Sugestões de temas ou assuntos")
    print("  • Qualquer outro comentário")
    print("\nA IA vai usar seu feedback para adaptar as próximas perguntas!\n")
    
    feedback = input(f"{STUDENT_NAME}: ").strip()
    
    if not feedback:
        feedback = "Sem feedback desta vez."
    
    return feedback


def generate_questions_with_ai(feedback: str) -> str:
    """
    Gera perguntas personalizadas usando a API do Gemini.
    
    Args:
        feedback: Feedback atual do usuário
    
    Returns:
        String com perguntas no formato QUESTION=...; EXPLAIN=...; ANSWER=...;
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Obtém feedbacks anteriores
    previous_feedbacks = get_feedbacks_text(max_count=MAX_FEEDBACKS)
    
    # Obtém matéria do dia
    subject = get_current_subject()
    
    # Monta o prompt
    prompt = f"""Você deve gerar perguntas no formato EXATAMENTE descrito abaixo, sem nunca quebrar nenhuma dessas regras. Sua única saída deve ser uma lista de perguntas, cada uma em single-line, seguindo todas as instruções. NÃO adicione introdução, explicações, comentários, saudações, markdown, nada além das perguntas. A única função desse prompt é gerar as perguntas para o programa R.A.F.F.

## REGRAS ABSOLUTAS E OBRIGATÓRIAS

### 1. Formato exato de cada pergunta (single-line)
Cada pergunta deve ser exatamente assim, em uma única linha:

QUESTION={{texto-da-pergunta}}; EXPLAIN={{texto-de-explicacao}}; ANSWER={{resposta}};

* Tudo na mesma linha.
* Apenas pule para a próxima linha para criar uma nova pergunta.
* Nunca use quebras de linha reais dentro do EXPLAIN.

### 2. Como quebrar linhas dentro do EXPLAIN
Para deixar o EXPLAIN mais bonito no programa sem quebrar o formato, use o texto literal '\\n', não a quebra real.

Exemplo correto:
EXPLAIN=Primeira linha.\\nSegunda linha.\\n\\nParágrafo novo;

(ou seja, barra + n escritos mesmo: '\\n')

### 3. Estilo do EXPLAIN
* Pode ser engraçado, leve, memorável, igual aos exemplos dados.
* Pode usar analogias, mini-histórias, sarcasmo leve.
* Nunca parecer tiozão ou infantil.
* Sempre escrito de forma clara e pedagógica.
* Use linguagem que engaje e motive o estudante.

EXEMPLO DE UMA PERGUNTA REAL:
QUESTION=x + 6 = 10 (equação incognita de primeiro grau); EXPLAIN=Achar o X é descobrir qual número faz a conta ficar verdadeira.\\nPara isso, deixamos o X sozinho de um lado da conta.\\n\\nO que estiver junto do X, passa para o outro lado fazendo a operação contrária. Isso quer dizer que a conta muda para o contrário do que estava antes.\\n\\nSe estiver somando, passa subtraindo.\\nExemplo: [x + 3 = 7] vira [x = 7 - 3]\\n\\nSe estiver subtraindo, passa somando.\\nExemplo: [x - 5 = 2] vira [x = 2 + 5]\\n\\nSe estiver multiplicando, passa dividindo.\\nExemplo: [3x = 12] vira [x = 12 / 3]\\n\\nSe estiver dividindo, passa multiplicando.\\nExemplo: [x / 4 = 3] vira [x = 3 * 4]\\n\\nO objetivo é deixar o X sozinho, e assim descobrir qual número ele representa.; ANSWER=4;

OUTRO EXEMPLO:
QUESTION=Qual é o resultado de 72 / 8?; EXPLAIN=Vamos pensar da seguinte forma:\\n\\nVocê precisa destruir o número 72 usando apenas múltiplos de 8, ou seja, números que conseguem se multiplicar com 8.\\n\\nPense que o 8 é tipo uma rainha, o 72 é um inimigo. Você vai precisar de soldados (qualquer número) para multiplicar com a rainha. O resultado é o ataque no inimigo, baixando o valor dele.\\n\\nNesse caso você tem 72 (inimigo) na zona de ataque e 8 (rainha) na zona de preparo.\\n\\nVocê precisa multiplicar números (soldados) por 8 (rainha) que aos poucos vão diminuindo o 72 até resultar em zero. Quando o inimigo for totalmente aniquilado para a destruição absoluta e certeira.\\n\\nNão se esquece de anotar os números (soldados) que você multiplicou com 8 (rainha), no fim você vai somar os soldados e aí você vai ter o resultado.\\n\\nAfinal, o time vai querer a lista de soldados que lutaram e a soma deles.; ANSWER=9;

Note como em alguns momentos foram usados '\\n\\n' para melhorar o conforto aos olhos enquanto lê o texto, para ter um espaçamento.

### 4. Conteúdo permitido
* Apenas caracteres normais de teclado (A–Z, 0–9, '.', ',', '?', '/', '*', '-', '+', '=', etc.)
* Pode usar símbolos como ², ³, $, %, #
* NUNCA usar emojis ou caracteres especiais fora do ASCII básico (para evitar quebra no terminal).

### 5. Quantidade de perguntas
Você deve produzir exatamente {AI_QUESTIONS_COUNT} perguntas. Nem mais, nem menos.

### 6. Tipo de perguntas
Com base no feedback do aluno, você deve:
* Ajustar dificuldade corretamente baseado nos feedbacks anteriores.
* Ajustar tom emocional para manter o engajamento.
* Repetir padrões de tópicos que o aluno teve dificuldade.
* Reforçar tópicos que funcionaram bem.
* Introduzir desafios graduais quando apropriado.
* Manter consistência temática com o aprendizado anterior.
* Adaptar-se à preferências e estilo de aprendizagem do aluno.

### 7. Referência para manter o estilo
Sempre siga o estilo, ritmo e nível dos EXPLAINS fornecidos, como:
* Linguagem leve e acessível
* Didática baseada em metáforas e analogias
* Pequenos elementos humorísticos quando apropriado
* Técnica ensinada + exemplo + reforço

### 8. Regras CRÍTICAS sobre ANSWER (MUITO IMPORTANTE!)

**REGRA DE OURO:** O estudante NUNCA deve ter que adivinhar uma resposta longa ou complexa!

**Tipos de respostas permitidas:**

A) **Respostas OBJETIVAS** (podem ser diretas):
   - Números: "4", "25", "3.14"
   - Cálculos matemáticos: "12", "-5", "100"
   - Operações: "x=4", "y=10"
   - Valores exatos e únicos

B) **Respostas SUBJETIVAS** (OBRIGATÓRIO usar múltipla escolha):
   - Conceitos: "O que é fotossíntese?"
   - Nomes próprios: "Qual a capital do Brasil?"
   - Palavras longas: "Nome do processo..."
   - Qualquer resposta com mais de 1 palavra
   - Textos, definições, explicações
   
**Para respostas subjetivas (B):**
   - SEMPRE use formato de múltipla escolha (a, b, c, d)
   - As opções DEVEM estar claramente no EXPLAIN
   - Use formato: "a) opção 1\\nb) opção 2\\nc) opção 3\\nd) opção 4"
   - O ANSWER deve ser APENAS a letra: "a" ou "b" ou "c" ou "d"
   - Aceite maiúsculas e minúsculas (o sistema compara sem case-sensitive)

**EXEMPLOS CORRETOS:**

CORRETO (resposta objetiva):
QUESTION=Quanto é 5 + 3?; EXPLAIN=Soma básica...; ANSWER=8;

CORRETO (múltipla escolha):
QUESTION=Qual a capital do Brasil?; EXPLAIN=Escolha a cidade:\\n\\na) Rio de Janeiro\\nb) São Paulo\\nc) Brasília\\nd) Salvador; ANSWER=c;

INCORRETO (NÃO FAÇA ISSO!):
QUESTION=Qual a capital do Brasil?; EXPLAIN=É a cidade onde...; ANSWER=Brasília;
☝️ Estudante teria que adivinhar "Brasília" exatamente = FRUSTRANTE!

**Outras regras de ANSWER:**
* Nunca use acentos no ANSWER se puder evitar
* Prefira letras minúsculas
* Mantenha curto (máximo 15 caracteres)
* O EXPLAIN pode ensinar o conceito mas NÃO deve dar a resposta direta

### 9. Referências culturais
* Você pode usar referências a cultura pop, nerd, geek, gamer para exemplificar.
* Mantenha as referências atuais e relevantes para adolescentes.

### 10. Formatação
* NÃO use formatações markdown (**negrito**, # títulos, etc.)
* Tudo será exibido em terminal CMD/PowerShell.

# CONTEXTO PARA PERSONALIZAÇÃO

**Aluno:** {STUDENT_NAME}

**Matéria de hoje:** {subject}

**Feedback atual:**
{feedback}

**Feedbacks anteriores (histórico de aprendizado):**
{previous_feedbacks}

**Quantidade de perguntas:** {AI_QUESTIONS_COUNT}

**Instrução especial:**
Se você for fazer exercícios de matemática, o EXPLAIN precisa ensinar como fazer a conta/operação. 
Ele precisa explicar a fórmula e o processo, mas NÃO deve dar a resposta direta.

**IMPORTANTE - Evite frustração:**
NUNCA faça perguntas onde o estudante precise adivinhar uma palavra/frase longa exata!
Se a resposta não for um número ou cálculo matemático, USE MÚLTIPLA ESCOLHA (a, b, c, d).
O estudante não deve ter que digitar "Brasília" exatamente - ele deve poder escolher "c".

# TAREFA FINAL
Gere exatamente {AI_QUESTIONS_COUNT} perguntas seguindo todas as regras acima.
Leve em consideração o histórico de feedbacks para adaptar dificuldade e estilo.
Produza apenas as perguntas, nada mais."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        questions_text = response.text.strip()
        
        # Salva o feedback
        add_feedback(feedback, max_feedbacks=MAX_FEEDBACKS)
        
        # Salva as perguntas geradas
        save_last_questions(questions_text)
        
        return questions_text
        
    except Exception as e:
        raise Exception(f"Erro ao gerar perguntas com IA: {e}")


def run_ai_feedback_flow() -> str:
    """
    Executa o fluxo completo de feedback e geração de perguntas.
    
    Returns:
        String com as perguntas geradas
    """
    feedback = collect_feedback()
    print("\n🤖 Gerando perguntas personalizadas com IA...\n")
    
    try:
        questions = generate_questions_with_ai(feedback)
        print("✅ Perguntas geradas com sucesso!\n")
        return questions
    except Exception as e:
        print(f"❌ Erro ao gerar perguntas: {e}")
        print("Usando perguntas anteriores...\n")
        from src.storage import get_last_questions
        return get_last_questions()
