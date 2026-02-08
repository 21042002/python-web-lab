from flask import Flask, render_template, request, redirect
import banco


app = Flask(__name__)

# Cria a tabela ao iniciar o projeto 
banco.criar_tabela()


# ===== ROTAS ======
@app.route("/")
def index():
    return render_template("index.html")

# Inseirndo dados na tabela
@app.route("/salvar", methods=["POST"])
def salvar():
    nome = request.form["nome"]
    email = request.form["email"]

    conn = banco.conectar()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?,?)",(nome, email))

    conn.commit()
    conn.close()

    return redirect("/listar")

# Selecionando dados da tabela 
@app.route("/listar")
def listar():
    conn = banco.conectar()
    cursor= conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    usuarios = cursor.fetchall()

    conn.close()

    return render_template("listar.html", usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)