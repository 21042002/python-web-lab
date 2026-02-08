import sqlite3

# Criação do banco de dados e tabela
def conectar():
    return sqlite3.connect("clientes.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL 
    )""")
    
    conn.commit()
    conn.close()
