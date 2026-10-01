import sqlite3


BANCO = "memoria.db"


def conectar():
    return sqlite3.connect(BANCO)


def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens_processadas (
            message_id TEXT PRIMARY KEY
        )
    """)

    conexao.commit()
    conexao.close()


def adicionar_mensagem(numero, papel, conteudo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO mensagens (
            numero,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            numero,
            papel,
            conteudo
        )
    )

    conexao.commit()
    conexao.close()


def obter_historico(numero):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM mensagens
        WHERE numero = ?
        ORDER BY id DESC
        LIMIT 10
        """,
        (numero,)
    )

    registros = cursor.fetchall()

    conexao.close()

    registros.reverse()

    historico = []

    for papel, conteudo in registros:
        historico.append({
            "role": papel,
            "content": conteudo
        })

    return historico


def mensagem_ja_processada(message_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT message_id
        FROM mensagens_processadas
        WHERE message_id = ?
        """,
        (message_id,)
    )

    resultado = cursor.fetchone()

    conexao.close()

    return resultado is not None


def marcar_mensagem_processada(message_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO mensagens_processadas (
            message_id
        )
        VALUES (?)
        """,
        (message_id,)
    )

    conexao.commit()
    conexao.close()


criar_banco()