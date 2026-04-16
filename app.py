from flask import Flask, request, render_template, redirect, url_for, session
import re
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "chave_secreta_senai"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "usopessoal"
}

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def senha_forte(s: str) -> bool:
    if len(s) < 8:
        return False
    if not re.search(r"[A-Za-z]", s):
        return False
    if not re.search(r"\d", s):
        return False
    return True

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/login")
def login_page():
    return render_template("login.html")

@app.get("/perfil")
def perfil():
    if "usuario_id" not in session:
        return redirect(url_for("login_page"))

    conn = None
    cur = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT * FROM usuarios WHERE id = %s",
            (session["usuario_id"],)
        )
        usuario = cur.fetchone()

        return render_template("perfil.html", usuario=usuario)

    except mysql.connector.Error as e:
        return f"Erro no banco: {e}", 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.post("/register")
def register():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    senha = request.form.get("password", "").strip()
    cpf = request.form.get("CPF", "").strip()
    endereco = request.form.get("Endereço", "").strip()
    estado = request.form.get("estado", "").strip()
    cidade = request.form.get("Cidade", "").strip()

    if len(nome) < 3:
        return "Nome inválido", 400
    if not EMAIL_RE.match(email):
        return "Email inválido", 400
    if not senha_forte(senha):
        return "Senha fraca", 400

    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    conn = None
    cur = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT id FROM usuarios WHERE email=%s", (email,))
        if cur.fetchone():
            return "Email já cadastrado", 400

        cur.execute("""
            INSERT INTO usuarios 
            (nome, email, senha, cpf, endereco, estado, cidade)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, email, senha_hash, cpf, endereco, estado, cidade))

        conn.commit()
        return redirect(url_for("login_page"))

    except mysql.connector.Error as e:
        return f"Erro no banco: {e}", 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.post("/login")
def login():
    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "").strip()

    conn = None
    cur = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        usuario = cur.fetchone()

        if not usuario:
            return "Usuário não encontrado", 404

        if not bcrypt.checkpw(senha.encode(), usuario["senha"].encode()):
            return "Senha incorreta", 401

        session["usuario_id"] = usuario["id"]
        return redirect(url_for("perfil"))

    except mysql.connector.Error as e:
        return f"Erro no banco: {e}", 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True)