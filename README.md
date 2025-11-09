# R.A.F.F
(Descrição pra ser feita)

### Placeholders e coisas para escrever no README
- Falar mais sobre as técnicas usadas, proposta, importância e storytelling pessoal e interface CLI, funcionamento

## Lista de tarefas (to-do)
- [ ] **Tarefas ainda para a V1/MVP** (essa)
  - [x] Adicionar fallback para uso offline em caso de erros
  - [x] Adicionar tratamentos de erros
  - [x] Melhorar a estrutura do _config.py
  - [x] Adicionar comentários mais úteis e claros
  - [x] Melhorar o .gitignore
  - [ ] Melhorar nome dos arquivos
  - [ ] Finalizar README com introdução, detalhes, instruções, troubleshoot e artigos.
  - [ ] Adicionar nome na janela .py (quando executado via processo, tipo `cmd` ou `taskschd`)
  - [ ] Melhorar tratamento de fechamento de janela (Windows)

<br>

- [ ] **Tarefas para a V2/RELEASE**
  - [ ] Criar uma versão instalável para Windows
  - [ ] Melhorar o sistema do var.txt (ou me livrar dele)
  - [ ] Implementar a versão GUI com customização de usuário (sons, imagens) usando o `.config`
  - [ ] Tirar a necessidade do uso do Task Scheduler do Windows (restart + periódico)

## Forma de usar até o momento (Windows)
Essa seção ta em construção, a escrita ta simplória.

1. Baixe o projeto

2. Entre na pasta raiz do projeto

3. Baixe as dependências com `pip install -r requirements.txt`

4. Configure o `_config.py` (eu uso pastebin no modo `Raw` na variável `URL` e `URLCHECK`)

5. Adicione uma tarefa no task scheduler do Windows e configure para ela executar o `_main.py` do projeto

6. Adicione os trigger ao seu bel-prazer: eu gosto de usar um a cada 2 horas e outro ao reiniciar o PC