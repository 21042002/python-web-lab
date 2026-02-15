# ============================================================
# main.py - Aplicacao Flask de Login e Cadastro de Usuarios
# ============================================================
# Este projeto implementa um sistema de autenticacao basico com:
#   - Tela de login (usuario entra com email e senha)
#   - Tela de cadastro (usuario cria uma conta nova)
#   - Validacao de dados no servidor
#   - Armazenamento seguro de senhas com hash (werkzeug)
#
# FLUXO DO SISTEMA:
#   1. Usuario acessa /login
#   2. Se ja tem conta -> digita email e senha -> sistema valida
#   3. Se nao tem conta -> clica em "Cadastrar" -> rota /cadastro
#   4. Apos cadastro -> redireciona para /login
#   5. Apos login valido -> redireciona para /dashboard
#
# Rotas:
#   GET  /login     -> Exibe formulario de login
#   POST /login     -> Processa os dados de login
#   GET  /cadastro  -> Exibe formulario de cadastro
#   POST /cadastro  -> Processa os dados de cadastro
#   GET  /dashboard -> Pagina protegida (so acessa logado)
# ============================================================

# Importacoes do Flask
from flask import Flask, request, redirect, render_template, url_for, flash, session
import os

# Importa o modulo de banco de dados (criado separadamente)
import banco

# ============================================================
# CRIACAO DA APLICACAO FLASK
# ============================================================
app = Flask(__name__)

# secret_key eh obrigatoria para usar:
#   - session (guardar dados do usuario logado)
#   - flash messages (mensagens temporarias de feedback)
# SEGURANCA: A chave vem de uma variavel de ambiente, NAO fica no codigo
# Como o repo eh PUBLICO, qualquer chave no codigo fica exposta!
# Para definir a variavel antes de rodar:
#   Linux/Mac: export SECRET_KEY="sua_chave_secreta_aqui"
#   Windows:   set SECRET_KEY=sua_chave_secreta_aqui
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-trocar-em-producao")

# ============================================================
# INICIALIZACAO DO BANCO DE DADOS
# ============================================================
# Cria a tabela de usuarios quando a aplicacao inicia
banco.criar_tabela()


# ============================================================
# ROTAS DA APLICACAO
# ============================================================

# ---- ROTA DE LOGIN ----
# Aceita GET (exibir formulario) e POST (processar login)
@app.route("/login", methods=["GET", "POST"])
def login():
    # Se o metodo eh GET -> apenas exibe a pagina de login
    if request.method == "GET":
        return render_template("login.html")

    # Se o metodo eh POST -> o usuario enviou o formulario
    # Pega os dados enviados pelo formulario HTML
    email = request.form["email"].strip()
    senha = request.form["senha"].strip()

    # Validacao: verifica se os campos nao estao vazios
    if not email or not senha:
        flash("Preencha todos os campos!", "danger")
        return redirect(url_for("login"))

    # Busca o usuario no banco de dados pelo email
    usuario = banco.buscar_usuario_por_email(email)

    # Verifica se o usuario existe E se a senha esta correta
    # banco.verificar_senha() compara a senha digitada com o hash salvo
    if usuario and banco.verificar_senha(usuario[2], senha):
        # Login bem-sucedido!
        # session eh um dicionario que guarda dados do usuario durante a navegacao
        # Os dados da session ficam salvos em um cookie criptografado no navegador
        session["usuario_id"] = usuario[0]
        session["usuario_nome"] = usuario[1]

        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("dashboard"))
    else:
        # Login falhou: email nao encontrado ou senha incorreta
        # IMPORTANTE: Nao diga qual dos dois esta errado (seguranca)
        # Se disser "email nao encontrado", um atacante sabe quais emails existem
        flash("Email ou senha incorretos!", "danger")
        return redirect(url_for("login"))


# ---- ROTA DE CADASTRO ----
# Aceita GET (exibir formulario) e POST (processar cadastro)
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    # Se o metodo eh GET -> apenas exibe a pagina de cadastro
    if request.method == "GET":
        return render_template("cadastro.html")

    # Se o metodo eh POST -> o usuario enviou o formulario de cadastro
    nome = request.form["nome"].strip()
    email = request.form["email"].strip()
    senha = request.form["senha"].strip()

    # Validacao: todos os campos sao obrigatorios
    if not nome or not email or not senha:
        flash("Preencha todos os campos!", "danger")
        return redirect(url_for("cadastro"))

    # Verifica se ja existe um usuario com esse email
    # Cada email deve ser unico no sistema
    usuario_existente = banco.buscar_usuario_por_email(email)
    if usuario_existente:
        flash("Este email ja esta cadastrado!", "danger")
        return redirect(url_for("cadastro"))

    # Insere o novo usuario no banco de dados
    # A senha eh convertida em hash dentro da funcao inserir_usuario()
    banco.inserir_usuario(nome, email, senha)

    flash("Cadastro realizado! Faca login.", "success")
    return redirect(url_for("login"))


# ---- ROTA DO DASHBOARD (AREA PROTEGIDA) ----
# So pode ser acessada por usuarios logados
@app.route("/dashboard")
def dashboard():
    # Verifica se o usuario esta logado checando a session
    # Se "usuario_id" nao esta na session, o usuario nao fez login
    if "usuario_id" not in session:
        flash("Faca login para acessar!", "danger")
        return redirect(url_for("login"))

    # Usuario esta logado -> exibe o dashboard
    # Passa o nome do usuario para o template
    return render_template("dashboard.html", nome=session["usuario_nome"])


# ---- ROTA DE LOGOUT ----
# Encerra a sessao do usuario (desloga)
@app.route("/logout")
def logout():
    # session.clear() remove todos os dados da sessao
    # O usuario precisara fazer login novamente
    session.clear()
    flash("Voce saiu da conta.", "success")
    return redirect(url_for("login"))


# ============================================================
# EXECUCAO DA APLICACAO
# ============================================================
if __name__ == "__main__":
    # debug=True -> modo desenvolvimento (recarrega ao salvar)
    # NUNCA use debug=True em producao!
    app.run(debug=True)


# ============================================================
# VULNERABILIDADES CONHECIDAS E COMO EVITAR
# ============================================================
#
# Vulnerabilidade 1: SQL INJECTION
#   O que eh: Atacante insere comandos SQL maliciosos nos campos do formulario
#   Exemplo: No campo email, digitar: ' OR 1=1 --
#   Como evitar: Usar parametros '?' no SQL (ja implementado no banco.py)
#
# Vulnerabilidade 2: SENHAS EM TEXTO PURO
#   O que eh: Salvar a senha exatamente como o usuario digitou
#   Risco: Se o banco for vazado, todas as senhas ficam expostas
#   Como evitar: Usar hash de senha com werkzeug (ja implementado)
#
# Vulnerabilidade 3: CROSS-SITE SCRIPTING (XSS)
#   O que eh: Atacante insere codigo JavaScript nos campos
#   Exemplo: No campo nome, digitar: <script>alert('hackeado')</script>
#   Como evitar: Jinja2 escapa HTML automaticamente ({{ variavel }})
#
# ============================================================
