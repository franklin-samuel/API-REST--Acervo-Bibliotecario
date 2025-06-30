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

def buscar_obra(id_obra):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM obras WHERE id = ?", (str(id_obra),))
    row = cursor.fetchone()
    conn.close()
    return row

def buscar_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (str(id_usuario),))
    row = cursor.fetchone()
    conn.close()
    return row

def atualizar_quantidade_obra(obra_id, value):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM obras WHERE id = ?", (str(obra_id),))
    row = cursor.fetchone()
    if row:
        new_value = row[0] + value
        if new_value > 0:
            cursor.execute("UPDATE obras SET quantidade = ? WHERE id = ?", (new_value, str(obra_id)))
        else: raise ValueError("Quantidade não pode ser negativa")
    conn.commit()
    conn.close()

def listar_todas_obras():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM obras")
    rows = cursor.fetchall()
    conn.close()
    return rows

def listar_usuarios_com_divida():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE divida > 0")
    rows = cursor.fetchall()
    conn.close()
    return rows

def historico_por_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emprestimos WHERE usuario_id = ?", (str(usuario_id),))
    rows = cursor.fetchall()
    conn.close()
    return rows

def buscar_emprestimo(id_emprestimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emprestimos WHERE id = ?", (str(id_emprestimo),))
    row = cursor.fetchone()
    conn.close()
    return row

def buscar_emprestimos_por_usuario(id_usuario):
    conn = sqlite3.connect("acervo.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            e.id, 
            e.id_obra, 
            e.data_emprestimo, 
            e.data_prev_dev, 
            e.data_devolucao,
            o.titulo
        FROM emprestimos e
        JOIN obras o ON e.id_obra = o.id
        WHERE e.id_usuario = ?
        ORDER BY e.data_emprestimo DESC
    """, (str(id_usuario),))

    resultados = cursor.fetchall()
    conn.close()
    return resultados