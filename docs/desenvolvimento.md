# Guia de Desenvolvimento — R.A.F.F

## Arquitetura do Sistema
O R.A.F.F é estruturado em módulos independentes:
- `raff.core`: Lógica de negócios, rede, agendador, segurança e persistência.
- `raff.gui`: Interface gráfica PyQt6, janelas de quiz, diálogos e System Tray.
- `raff.api`: API REST local com FastAPI e Uvicorn.
- `raff.cli`: Comandos de linha de comando para automação.

## Executando os Testes
Para rodar a suíte de testes unitários:
```bash
pytest
```

## Verificação de Integridade
Para checar configurações e dependências:
```bash
python healthcheck.py
```
