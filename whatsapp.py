import os
import re
import requests

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SYSTEM_USER_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v26.0")


def normalizar_numero(numero):
    """
    Corrige números brasileiros recebidos pelo webhook
    sem o 9º dígito.

    Exemplo:
    558582141730
    vira
    5585982141730
    """

    numero = re.sub(r"\D", "", numero)

    # Brasil = 55
    # Se tiver 12 dígitos, insere o 9 depois do DDD.
    if numero.startswith("55") and len(numero) == 12:
        numero = numero[:4] + "9" + numero[4:]

    return numero


def enviar_mensagem_whatsapp(numero, mensagem):

    numero_original = numero
    numero = normalizar_numero(numero)

    print("Número recebido do webhook:", numero_original)
    print("Número usado para resposta:", numero)

    url = (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/"
        f"{PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    dados = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }

    resposta = requests.post(
        url,
        headers=headers,
        json=dados,
        timeout=30
    )

    print("Status Meta:", resposta.status_code)
    print("Resposta Meta:", resposta.text)

    if not resposta.ok:
        raise Exception(
            f"Erro da Meta {resposta.status_code}: {resposta.text}"
        )

    return resposta.json()