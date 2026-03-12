from flask import Flask, request, jsonify, render_template, redirect, url_for
import re
import mysql.connector
import bcrypt

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "usopessoal"
}

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def senha_forte(s: str) -> bool:
    print(f"Senha recebida para validar: '{s}'") # Debug: veja o que chega aqui
    if len(s) < 8:
        return False
    # Verifica se tem pelo menos uma letra
    if not re.search(r"[a-zA-Z]", s):
        return False
    # Verifica se tem pelo menos um número
    if not re.search(r"\d", s):
        return False
    return True

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/register")
def register():
    # recebe dados do FORM (HTML)
    nome = (request.form.get("nome")).strip()
    email = (request.form.get("email")).strip()
    senha = (request.form.get("password")).strip()

    if len(nome) < 3:
        return "Nom dever ter pelo menos 3 caracteres.", 400
    if not EMAIL_RE.match(email):
        return "Email invalido.", 400
    if not senha_forte(senha):
        return "Senha fraca. Use 8+ caracteres, com letras e numeros.", 400
    
    senha = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT id FROM usuarios WHERE email=%s", (email,))
        if cur.fetchone():
            return "Esse email já esta cadastrado.", 400
        
        cur.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            (nome, email, senha)
        )
        conn.commit()

        return redirect(url_for("home"))
    
    except mysql.connector.Error as e:
        return f"Erro no banco de dados: {e}", 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)