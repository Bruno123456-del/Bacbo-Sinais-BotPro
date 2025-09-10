import sqlite3

DB_NAME = "bot.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    conn = conectar()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        vip INTEGER DEFAULT 0,
        pontos INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS depositos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        valor REAL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def adicionar_usuario(user_id, nome):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO usuarios (id, nome) VALUES (?, ?)", (user_id, nome))
    conn.commit()
    conn.close()

def atualizar_vip(user_id, status):
    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE usuarios SET vip=? WHERE id=?", (status, user_id))
    conn.commit()
    conn.close()

def adicionar_pontos(user_id, pontos):
    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE usuarios SET pontos = pontos + ? WHERE id=?", (pontos, user_id))
    conn.commit()
    conn.close()

def pegar_ranking(limit=5):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT nome, pontos FROM usuarios ORDER BY pontos DESC LIMIT ?", (limit,))
    top = c.fetchall()
    conn.close()
    return top
