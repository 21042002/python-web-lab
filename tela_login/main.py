from flask import Flask, request, redirect, render_template

# Realizar a importação do banco de dados


app =  Flask(__name__)

# passo 1: sincronizar com o banco de dados para receber informações

# passo 2: acessando a rota /login
@app.route("/login")
def login(username, email):
    pass
    # passo 2.1: Pegando os dados dos inputs
    # passo 2.2: Validando os dados 
    # passo 2.3: envinado os dados para o banco de dados

# passo 3: acessando a rota email, senha para ter acesso as informações



# passo 4: verificar se os dados já existem dentro do banco

# passo 5: liberar acesso ao usuario

# passo 6: Se o cliente acessar direconar para a rota de acesso.

# ====== PASSOS ALTERNATIVOS ==========
# passo 1: Se o cliente não tiver cadastro criar rota de cadastro

if __name__ == '__main__':
    app.run(debug=True)

# ======= VUNERABILIDADES ========
# VUNERABILIDADES QUE PODEM EXISTE: 

# Vunera. 1:
# Vunera. 2:
# Vunera. 3:

