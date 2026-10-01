from datetime import datetime


ARQUIVO_HISTORICO = "historico.txt"


def salvar_conversa(numero, mensagem, resposta):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    registro = (
        f"[{data_hora}]\n"
        f"Número: {numero}\n"
        f"Cliente: {mensagem}\n"
        f"Bot: {resposta}\n"
        f"{'-' * 50}\n"
    )

    with open(
        ARQUIVO_HISTORICO,
        "a",
        encoding="utf-8"
    ) as arquivo:
        arquivo.write(registro)