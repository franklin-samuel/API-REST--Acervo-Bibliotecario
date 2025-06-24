import sqlite3

def conectar():
    return sqlite3.connect("acervo.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        divida REAL DEFAULT 0)
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS obras (
        id TEXT PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano INTEGER,
        categoria TEXT,
        quantidade INTEGER,  
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emprestimos (
        id TEXT PRIMARY KEY,
        obra_id TEXT,
        usuario_id TEXT,
        data_emprestimo TEXT,
        data_prevista TEXT,
        data_devolucao TEXT
        )
        """)

    conn.commit()
    conn.close()
    