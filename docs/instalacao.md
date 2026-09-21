# Guia de Instalação — R.A.F.F

O **R.A.F.F** (Rotina de Aprendizado Focada e Flexível) pode ser instalado de diferentes formas no Windows 10 e 11.

---

## 1. Instalador Oficial (.msi)
A forma recomendada para a maioria das famílias e responsáveis:
1. Baixe o instalador `RAFF-2.0.0-Setup.msi` na aba de Releases.
2. Dê um duplo clique e siga as instruções do assistente.
3. O R.A.F.F será instalado e configurado para iniciar automaticamente na bandeja do sistema (System Tray).

---

## 2. Versão Portátil (.zip)
Ideal para uso sem necessidade de permissões de administrador no Windows:
1. Baixe `RAFF-2.0.0-Portavel.zip`.
2. Extraia o conteúdo em uma pasta de sua preferência (ex: `C:\RAFF`).
3. Execute `raff.exe` para iniciar.

---

## 3. Instalação para Desenvolvedores (Código-fonte)
Se preferir rodar direto pelo código em Python:
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/messias-autismhelper.git
cd messias-autismhelper

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
pip install -e .

# 4. Inicie o R.A.F.F
raff start
```
