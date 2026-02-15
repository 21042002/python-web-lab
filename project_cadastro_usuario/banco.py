# ============================================================
# banco.py - Modulo responsavel pela conexao com o banco de dados
# ============================================================
# Este arquivo centraliza todas as operacoes do banco de dados
# usando SQLite3, que eh um banco de dados leve e embutido
# no Python (nao precisa instalar nada extra).
#
# Funcoes disponiveis:
#   - conectar()    -> abre conexao com o banco
#   - criar_tabela() -> cria a tabela de clientes se nao existir
#   - inserir_cliente(nome, email) -> insere um novo cliente
#   - listar_clientes() -> retorna todos os clientes cadastrados
# ============================================================

import sqlite3
import os

# Nome do arquivo do banco de dados SQLite
# O banco fica salvo como um arquivo .db na pasta do projeto
BANCO_DE_DADOS = "clientes.db"


def conectar():
    """
    # Funcao que cria e retorna uma conexao com o banco de dados
    # O sqlite3.connect() faz duas coisas:
    #   1. Se o arquivo 'clientes.db' NAO existe -> cria o arquivo
    #   2. Se o arquivo JA existe -> apenas abre a conexao
    #
    # Retorna: objeto de conexao (conn) que sera usado para executar comandos SQL
    """
    # Monta o caminho completo do banco na mesma pasta deste arquivo
    caminho = os.path.join(os.path.dirname(__file__), BANCO_DE_DADOS)

    # Cria a conexao com o banco de dados
    conn = sqlite3.connect(caminho)

    return conn


def criar_tabela():
    """
    # Funcao que cria a tabela 'clientes' caso ela ainda nao exista
    # O comando 'CREATE TABLE IF NOT EXISTS' garante que:
    #   - Se a tabela NAO existe -> cria ela
    #   - Se a tabela JA existe -> nao faz nada (evita erro)
    #
    # Estrutura da tabela 'clientes':
    #   - id    : numero unico gerado automaticamente (chave primaria)
    #   - nome  : texto obrigatorio com o nome do cliente
    #   - email : texto obrigatorio com o email do cliente
    """
    # Abre uma conexao com o banco
    conn = conectar()

    # Cria um cursor - eh ele que executa os comandos SQL
    cursor = conn.cursor()

    # Executa o comando SQL para criar a tabela
    # O triple-quote (aspas triplas) permite escrever SQL em varias linhas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # commit() salva as alteracoes no banco de dados
    # Sem o commit, as mudancas seriam perdidas
    conn.commit()

    # close() fecha a conexao para liberar recursos
    # Sempre feche a conexao quando terminar de usar
    conn.close()


def inserir_cliente(nome, email):
    """
    # Funcao que insere um novo cliente no banco de dados
    # Recebe o nome e email como parametros
    #
    # IMPORTANTE: Usa parametros '?' ao inves de concatenar strings
    # Isso previne ataques de SQL Injection, que eh quando alguem
    # tenta inserir codigo SQL malicioso nos campos do formulario
    #
    # Parametros:
    #   - nome  : string com o nome do cliente
    #   - email : string com o email do cliente
    """
    # Abre conexao com o banco
    conn = conectar()
    cursor = conn.cursor()

    # INSERT INTO -> insere uma nova linha na tabela
    # VALUES (?, ?) -> os '?' sao substituidos pelos valores de forma segura
    cursor.execute(
        "INSERT INTO clientes (nome, email) VALUES (?, ?)",
        (nome, email)
    )

    # Salva a insercao no banco
    conn.commit()

    # Fecha a conexao
    conn.close()


def listar_clientes():
    """
    # Funcao que busca e retorna todos os clientes do banco
    # SELECT * FROM clientes -> seleciona todas as colunas de todos os registros
    # fetchall() -> pega todos os resultados e retorna como lista de tuplas
    #
    # Exemplo de retorno:
    #   [(1, 'Anderson', 'anderson@email.com'), (2, 'Maria', 'maria@email.com')]
    #   Cada tupla: (id, nome, email)
    #
    # Retorna: lista de tuplas com os dados dos clientes
    """
    # Abre conexao com o banco
    conn = conectar()
    cursor = conn.cursor()

    # Executa o SELECT para buscar todos os clientes
    cursor.execute("SELECT * FROM clientes")

    # fetchall() transforma o resultado em uma lista Python
    clientes = cursor.fetchall()

    # Fecha a conexao
    conn.close()

    # Retorna a lista de clientes
    return clientes
