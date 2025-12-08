from google import genai
from _config import GEMINI_APIKEY, NAME

client = genai.Client(api_key=GEMINI_APIKEY)
aimodel = "gemini-2.5-flash"
#baseprompt = f"Meu nome é {NAME}, o último prompt foi" #{LASTPROMPT}
baseprompt = "Quanto é 1+1?"

# ------------------------------------------------------------------------------------ #

# Mostrar código, README do Github, modelo acima e regras escritas por mim agora

# Sua função é pegar o feedback do aluno e gerar perguntas (no modelo citado acima) para ele fazer na próxima vez
# Não quero formatação, somente plaintext nas suas respostas, não me dê saudações nem nada, quero somente o output no modelo de perguntas abaixo

# Tem que ser EXATAMENTE igual o modelo de perguntas diz: (instruções)
# A quantidade de perguntas que você deve fazer é: {perguntas}
# Esse é o feedback do aluno: {feedback-atual}
# O prompt da última vez tinha sido: {ultimo-feedback}

# ------------------------------------------------------------------------------------ #

response = client.models.generate_content(
     model=aimodel, contents=f"{baseprompt} ABC"
 )
save = response.text
print(save)