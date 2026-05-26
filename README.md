# QR Code Generator

Servico simples em FastAPI para gerar e exibir QR Code de conexao WhatsApp a partir da Evolution API.

## O que este projeto mostra

- Endpoint web com FastAPI.
- Integracao com API externa via variaveis de ambiente.
- Tela HTML simples para exibir QR Code de conexao.
- Fluxo de reset/recriacao de instancia quando necessario.

## Stack

- Python
- FastAPI
- Requests
- Evolution API

## Variaveis de ambiente

```bash
EVOLUTION_URL=
EVOLUTION_KEY=
```

## Como rodar

```bash
pip install fastapi uvicorn requests
uvicorn main:app --reload
```

## Observacao

Projeto utilitario para conexao e diagnostico de instancia WhatsApp. Nao armazene chaves sensiveis no repositorio.
