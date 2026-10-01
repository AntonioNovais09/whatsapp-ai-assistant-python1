import requests

from config import INFORMACOES_EMPRESA


def gerar_resposta(mensagem, historico=None):
    url = "http://localhost:11434/api/chat"

    instrucao = f"""
Você é o atendente virtual de uma empresa.

INFORMAÇÕES OFICIAIS DA EMPRESA:

{INFORMACOES_EMPRESA}

REGRAS:

- Responda sempre em português.
- Use somente as informações oficiais da empresa.
- Não invente informações.
- Responda de forma curta, natural e educada.
- Considere o histórico da conversa para entender perguntas complementares.
- Se a informação não existir, responda:
"Não tenho essa informação no momento. Posso encaminhar sua dúvida para um atendente."
"""

    mensagens = [
        {
            "role": "system",
            "content": instrucao
        }
    ]

    if historico:
        mensagens.extend(historico)

    mensagens.append({
        "role": "user",
        "content": mensagem
    })

    dados = {
        "model": "llama3.2:3b",
        "messages": mensagens,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    resposta = requests.post(
        url,
        json=dados,
        timeout=60
    )

    resposta.raise_for_status()

    resultado = resposta.json()

    return resultado["message"]["content"].strip()