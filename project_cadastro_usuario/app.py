# ============================================================
# app.py - Arquivo principal da aplicacao Flask
# ============================================================
# Este eh o ponto de entrada da aplicacao web.
# Aqui ficam definidas todas as ROTAS (URLs) que o usuario
# pode acessar no navegador.
#
# O Flask funciona assim:
#   1. O usuario acessa uma URL no navegador (ex: http://localhost:5000/)
#   2. O Flask verifica qual funcao corresponde a essa URL
#   3. A funcao processa a requisicao e retorna uma resposta (HTML)
#
# Rotas deste projeto:
#   GET  "/"       -> Exibe o formulario de cadastro
#   POST "/salvar" -> Recebe os dados do formulario e salva no banco
#   GET  "/listar" -> Exibe a lista de todos os clientes cadastrados
# ============================================================

# Importacoes do Flask:
# - Flask: classe principal que cria a aplicacao web
# - render_template: funcao que renderiza arquivos HTML da pasta 'templates/'
# - request: objeto que contem os dados enviados pelo usuario (formularios, URL, etc)
# - redirect: funcao que redireciona o usuario para outra pagina
# - url_for: funcao que gera URLs dinamicamente a partir do nome da funcao
#   (melhor que escrever URLs fixas como "/listar", pois se mudar a URL nao quebra)
# - flash: funcao que envia mensagens temporarias para o usuario (feedback)
from flask import Flask, render_template, request, redirect, url_for, flash
import os

# Importa o modulo banco.py que criamos para lidar com o banco de dados
import banco

# ============================================================
# CRIACAO DA APLICACAO FLASK
# ============================================================
# Flask(__name__) cria a aplicacao web
# __name__ eh uma variavel especial do Python que contem o nome do modulo atual
# O Flask usa isso para saber onde encontrar as pastas 'templates/' e 'static/'
app = Flask(__name__)

# secret_key eh necessaria para usar flash messages (mensagens temporarias)
# SEGURANCA: A chave vem de uma variavel de ambiente, NAO fica no codigo
# Para definir a variavel antes de rodar:
#   Linux/Mac: export SECRET_KEY="sua_chave_secreta_aqui"
#   Windows:   set SECRET_KEY=sua_chave_secreta_aqui
# Ou crie um arquivo .env (que deve estar no .gitignore)
# os.environ.get() busca a variavel; se nao existir, usa o valor padrao
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-trocar-em-producao")

# ============================================================
# INICIALIZACAO DO BANCO DE DADOS
# ============================================================
# Cria a tabela 'clientes' no banco de dados quando a aplicacao inicia
# Se a tabela ja existe, nao faz nada (por causa do IF NOT EXISTS no SQL)
banco.criar_tabela()


# ============================================================
# ROTAS DA APLICACAO
# ============================================================

# ---- ROTA PRINCIPAL (PAGINA INICIAL) ----
# @app.route("/") eh um 'decorator' que conecta a URL "/" a funcao index()
# Quando alguem acessa http://localhost:5000/ o Flask executa a funcao index()
# methods=["GET"] eh o padrao - significa que essa rota so aceita leitura
@app.route("/")
def index():
    # render_template() procura o arquivo 'index.html' dentro da pasta 'templates/'
    # e retorna o HTML renderizado para o navegador do usuario
    return render_template("index.html")


# ---- ROTA PARA SALVAR CLIENTE ----
# methods=["POST"] significa que essa rota so aceita envio de dados (formulario)
# POST eh usado quando queremos ENVIAR dados para o servidor
# GET eh usado quando queremos RECEBER/VER dados do servidor
@app.route("/salvar", methods=["POST"])
def salvar():
    # request.form eh um dicionario com os dados enviados pelo formulario HTML
    # request.form["nome"] pega o valor do campo <input name="nome">
    # strip() remove espacos em branco extras no inicio e fim do texto
    nome = request.form["nome"].strip()
    email = request.form["email"].strip()

    # Validacao basica: verifica se os campos nao estao vazios
    # Mesmo com 'required' no HTML, eh importante validar no servidor tambem
    # porque alguem pode burlar a validacao do navegador
    if not nome or not email:
        # flash() envia uma mensagem temporaria que aparece na proxima pagina
        # "danger" eh a categoria da mensagem (usada para estilizar com CSS)
        flash("Preencha todos os campos!", "danger")
        return redirect(url_for("index"))

    # Chama a funcao do banco.py para inserir o cliente
    # A logica do banco fica separada no modulo banco.py (separacao de responsabilidades)
    banco.inserir_cliente(nome, email)

    # Envia mensagem de sucesso para o usuario
    flash("Cliente cadastrado com sucesso!", "success")

    # redirect() redireciona o navegador para outra URL
    # url_for("listar") gera a URL da funcao listar() automaticamente
    # Isso eh melhor que usar redirect("/listar") porque se mudar a URL
    # da rota, o url_for continua funcionando corretamente
    return redirect(url_for("listar"))


# ---- ROTA PARA LISTAR CLIENTES ----
# Rota GET (padrao) - apenas exibe informacoes
@app.route("/listar")
def listar():
    # Busca todos os clientes do banco de dados usando a funcao do banco.py
    # Retorna uma lista de tuplas: [(id, nome, email), ...]
    usuarios = banco.listar_clientes()

    # Renderiza o template 'listar.html' passando a lista de usuarios
    # No HTML, a variavel 'usuarios' estara disponivel para uso com Jinja2
    return render_template("listar.html", usuarios=usuarios)


# ============================================================
# EXECUCAO DA APLICACAO
# ============================================================
# __name__ == "__main__" verifica se este arquivo esta sendo executado diretamente
# (e nao importado como modulo por outro arquivo)
# Isso permite que o arquivo seja usado tanto como aplicacao quanto como modulo
if __name__ == "__main__":
    # app.run() inicia o servidor web Flask
    # debug=True ativa o modo de desenvolvimento:
    #   - Recarrega automaticamente quando voce salva alteracoes no codigo
    #   - Mostra mensagens de erro detalhadas no navegador
    #   ATENCAO: Nunca use debug=True em producao (ambiente real)!
    app.run(debug=True)
