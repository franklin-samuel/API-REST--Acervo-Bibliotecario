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
        quantidade INTEGER  
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

def salvar_usuario(usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (id, nome, email, divida)
        values (?, ?, ?, ?)
        """, (str(usuario.id), usuario.nome, usuario.email, usuario.divida))
    conn.commit()
    conn.close()

def salvar_obra(obra):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT quantidade FROM obras WHERE id = ?", (str(obra.id),))
    resultado = cursor.fetchone()

    if resultado:
        novo_quantidade = resultado[0] + obra.quantidade
        cursor.execute("UPDATE obras set quantidade = ? WHERE id = ?", (novo_quantidade, (str(obra.id))))
    else:
        cursor.execute("""
            INSERT INTO obras (id, titulo, autor, ano, categoria, quantidade)
            values (?, ?, ?, ?, ?, ?)
            """, (str(obra.id), obra.titulo, obra.autor, obra.ano, obra.categoria, obra.quantidade))
    conn.commit()
    conn.close()

def salvar_emprestimo(emprestimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emprestimos (id, obra_id, usuario_id, data_emprestimo, data_prevista, data_devolucao)
                   values (?, ?, ?, ?, ?, ?)
        """,
        (
            str(emprestimo.id),
            str(emprestimo.obra.id),
            str(emprestimo.usuario.id),
            emprestimo.data_emprestimo.isoformat(),
            emprestimo.previsao.isoformat(),
            getattr(emprestimo, 'data_devolucao', None)
        )
    )
    conn.commit()
    conn.close()

def registrar_devolucao(emprestimo_id, data_devolucao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE emprestimos SET data_devolucao = ?
        WHERE id = ?
    """, (data_devolucao.isoformat(), str(emprestimo_id)))
    conn.commit()
    conn.close()

def limpar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios")
    cursor.execute("DELETE FROM obras")
    cursor.execute("DELETE FROM emprestimos")

    conn.commit()
    conn.close()