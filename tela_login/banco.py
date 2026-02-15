# ============================================================
# banco.py - Modulo de banco de dados para o sistema de login
# ============================================================
# Gerencia todas as operacoes do banco de dados de usuarios.
# Usa SQLite3 para armazenamento e werkzeug para hash de senhas.
#
# IMPORTANTE sobre seguranca de senhas:
#   - NUNCA salve senhas em texto puro no banco de dados
#   - Sempre use hash (funcao que transforma a senha em texto irreversivel)
#   - werkzeug.security fornece funcoes seguras para isso
#
# Funcoes:
#   - conectar()                -> abre conexao com o banco
#   - criar_tabela()            -> cria a tabela de usuarios
#   - inserir_usuario()         -> cadastra um novo usuario
#   - buscar_usuario_por_email() -> busca usuario pelo email
#   - verificar_senha()         -> compara senha com hash
# ============================================================

import sqlite3
import os

# werkzeug ja vem instalado com o Flask (eh uma dependencia)
# generate_password_hash: transforma a senha em um hash seguro
# check_password_hash: verifica se uma senha corresponde ao hash
from werkzeug.security import generate_password_hash, check_password_hash

# Nome do arquivo do banco de dados
BANCO_DE_DADOS = "usuarios.db"


def conectar():
    """
    # Cria e retorna uma conexao com o banco de dados SQLite
    # O arquivo 'usuarios.db' eh criado automaticamente se nao existir
    """
    # Monta o caminho completo do banco na mesma pasta deste arquivo
    caminho = os.path.join(os.path.dirname(__file__), BANCO_DE_DADOS)
    conn = sqlite3.connect(caminho)
    return conn


def criar_tabela():
    """
    # Cria a tabela 'usuarios' se ela ainda nao existir
    #
    # Estrutura da tabela:
    #   - id    : identificador unico (gerado automaticamente)
    #   - nome  : nome do usuario (obrigatorio)
    #   - email : email do usuario (obrigatorio e unico)
    #   - senha : hash da senha (NUNCA a senha em texto puro!)
    #
    # UNIQUE(email): garante que nao existam dois usuarios com mesmo email
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def inserir_usuario(nome, email, senha):
    """
    # Insere um novo usuario no banco de dados
    #
    # PROCESSO DE SEGURANCA DA SENHA:
    #   1. Usuario digita a senha: "minhasenha123"
    #   2. generate_password_hash() transforma em algo como:
    #      "pbkdf2:sha256:260000$abc123$def456..."
    #   3. Esse hash eh salvo no banco (nao a senha original)
    #   4. Eh impossivel recuperar a senha original a partir do hash
    #
    # Parametros:
    #   - nome  : nome do usuario
    #   - email : email do usuario
    #   - senha : senha em texto puro (sera convertida em hash)
    """
    conn = conectar()
    cursor = conn.cursor()

    # Gera o hash da senha antes de salvar no banco
    # O hash inclui um "salt" (valor aleatorio) que torna cada hash unico
    # Mesmo que dois usuarios tenham a mesma senha, os hashes serao diferentes
    senha_hash = generate_password_hash(senha)

    # Insere os dados no banco usando parametros '?' (previne SQL Injection)
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
        (nome, email, senha_hash)
    )

    conn.commit()
    conn.close()


def buscar_usuario_por_email(email):
    """
    # Busca um usuario no banco de dados pelo email
    #
    # Retorna:
    #   - Tupla (id, nome, senha_hash) se encontrar o usuario
    #   - None se o email nao existir no banco
    #
    # fetchone() retorna apenas o primeiro resultado (ou None se nao encontrar)
    """
    conn = conectar()
    cursor = conn.cursor()

    # Busca o usuario pelo email
    cursor.execute(
        "SELECT id, nome, senha FROM usuarios WHERE email = ?",
        (email,)  # Virgula necessaria para criar uma tupla com 1 elemento
    )

    # fetchone() retorna uma tupla ou None
    usuario = cursor.fetchone()

    conn.close()
    return usuario


def verificar_senha(senha_hash, senha_digitada):
    """
    # Verifica se a senha digitada corresponde ao hash salvo no banco
    #
    # check_password_hash() faz o seguinte:
    #   1. Pega a senha digitada pelo usuario
    #   2. Aplica o mesmo algoritmo de hash
    #   3. Compara com o hash salvo no banco
    #   4. Retorna True se bater, False se nao
    #
    # Parametros:
    #   - senha_hash    : hash salvo no banco de dados
    #   - senha_digitada: senha que o usuario digitou no formulario
    #
    # Retorna: True (senha correta) ou False (senha incorreta)
    """
    return check_password_hash(senha_hash, senha_digitada)
