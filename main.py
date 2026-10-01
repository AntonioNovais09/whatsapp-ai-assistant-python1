import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, BackgroundTasks
from pydantic import BaseModel

from historico import salvar_conversa
from ia import gerar_resposta
from memoria import (
    obter_historico,
    adicionar_mensagem,
    mensagem_ja_processada,
    marcar_mensagem_processada
)
from whatsapp import enviar_mensagem_whatsapp


load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


class Mensagem(BaseModel):
    mensagem: str


@app.get("/")
def inicio():
    return {
        "status": "online",
        "mensagem": "API do WhatsApp IA funcionando"
    }


@app.post("/chat")
def chat(dados: Mensagem):
    numero = "teste-local"

    try:
        historico = obter_historico(numero)

        resposta = gerar_resposta(
            dados.mensagem,
            historico
        )

        adicionar_mensagem(
            numero,
            "user",
            dados.mensagem
        )

        adicionar_mensagem(
            numero,
            "assistant",
            resposta
        )

        salvar_conversa(
            numero,
            dados.mensagem,
            resposta
        )

        return {
            "mensagem": dados.mensagem,
            "resposta": resposta
        }

    except Exception as erro:
        print("Erro:", erro)

        return {
            "erro": "Não foi possível gerar uma resposta."
        }


@app.get("/webhook")
async def verificar_webhook(request: Request):
    modo = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    desafio = request.query_params.get("hub.challenge")

    if modo == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verificado com sucesso!")

        return Response(
            content=desafio,
            media_type="text/plain"
        )

    return Response(
        content="Falha na verificação do webhook",
        status_code=403
    )


def processar_mensagem(numero, texto):
    try:
        print("Mensagem:", texto)

        historico = obter_historico(numero)

        resposta_ia = gerar_resposta(
            texto,
            historico
        )

        adicionar_mensagem(
            numero,
            "user",
            texto
        )

        adicionar_mensagem(
            numero,
            "assistant",
            resposta_ia
        )

        salvar_conversa(
            numero,
            texto,
            resposta_ia
        )

        resultado_whatsapp = enviar_mensagem_whatsapp(
            numero,
            resposta_ia
        )

        print("Resposta da IA:", resposta_ia)
        print("Resposta enviada ao WhatsApp!")
        print(resultado_whatsapp)

    except Exception as erro:
        print("Erro ao processar mensagem:", erro)


@app.post("/webhook")
async def receber_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    dados = await request.json()

    try:
        mensagem = (
            dados["entry"][0]
            ["changes"][0]
            ["value"]
            ["messages"][0]
        )

        if mensagem.get("type") != "text":
            return {
                "status": "ignorado"
            }

        message_id = mensagem["id"]

        if mensagem_ja_processada(message_id):
            print("Mensagem duplicada ignorada.")

            return {
                "status": "duplicada"
            }

        numero = mensagem["from"]
        texto = mensagem["text"]["body"]

        marcar_mensagem_processada(message_id)

        background_tasks.add_task(
            processar_mensagem,
            numero,
            texto
        )

        return {
            "status": "recebido"
        }

    except KeyError:
        return {
            "status": "evento_ignorado"
        }

    except Exception as erro:
        print("Erro no webhook:", erro)

        return {
            "status": "erro"
        }