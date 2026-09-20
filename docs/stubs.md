# Suporte a Stubs e URLs Legadas

Nas versões anteriores (v1.x), o R.A.F.F utilizava endpoints remotos como Pastebin para carregar perguntas em texto simples.

---

## Compatibilidade Retroativa
A versão 2.0.0 mantém os parâmetros `URL_QUESTIONS` e `URL_CHECK` em `config.py` por compatibilidade com instalações existentes. No entanto, recomenda-se:
- Utilizar o **Banco Local de Questões** integrado (offline e seguro).
- Ou utilizar a integração nativa com a **API Gemini** para geração dinâmica.
