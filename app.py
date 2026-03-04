
# IMPORTAÇÕES
from flask import Flask, request , jsonify # Framework Flask + manipulação de requisição e resposta JSON
# Flask → cria a aplicação web
# request → pega dados enviados pelo cliente (Postman, navegador)
#jsonify → transforma dicionário Python em resposta JSON

from models.user import User # Modelo da tabela User (ORM) 
#Importa seu modelo de usuário (classe que representa a tabela no banco).

from database import db # Importa o objeto do SQLAlchemy, que controla o banco de dados.

# Sistema de autenticação e sessão
from flask_login import LoginManager, login_user, current_user, logout_user, login_required 
# LoginManager → gerencia autenticação
# login_user() → faz login do usuário
# current_user → usuário logado
# logout_user() → encerra sessão
# login_required → protege rotas


# Apenas para confirmar que o arquivo está sendo executado
print("APP INICIANDO...")

# CRIAÇÃO DA APLICAÇÃO

# Cria a aplicação Flask
app = Flask(__name__) 

# Chave secreta usada para proteger sessão e cookies
app.config['SECRET_KEY'] = "sua_chave_secreta" 

# Configuração do banco de dados (SQLite local)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/users' # Substitua 'senha' pela senha do seu MySQL


# CONFIGURAÇÃO DO LOGIN E BANCO
login_manager = LoginManager() # Cria gerenciador de login

db.init_app(app) # Conecta o banco à aplicação
login_manager.init_app(app) # Conecta o sistema de login à aplicação

# Define para qual rota o usuário será redirecionado se não estiver logado
login_manager.login_view = 'login'

# FUNÇÃO OBRIGATÓRIA DO FLASK-LOGIN
# CARREGAR USUÁRIO LOGADO
@login_manager.user_loader
def load_user(user_id):

    # Essa função é chamada automaticamente pelo Flask-Login. Ela recebe o ID salvo na sessão e retorna o usuário correspondente no banco.
    return User.query.get(user_id)

# ROTAS
# LOGIN
@app.route('/login', methods=['POST'])
def login():
    
    # Recebe username e password via JSON Verifica no banco se e válido, cria sessão de login.

    data = request.get_json() # Pega o JSON enviado pelo Postman.

    username = data.get("username") # Extrai dados do JSON.
    password = data.get("password") #-----------------
    
    if username and password:

        # Busca usuário no banco pelo username
        user = User.query.filter_by(username=username).first()

        # Verifica se usuário existe e senha confere
        if user and user.password == password:
            login_user(user) # Cria sessão
            print(current_user.is_authenticated)
            return jsonify({"Menssagem": "Autenticacao realizada com sucesso"}), 200
    
    return jsonify({"Menssagem": "Credenciais Invalida"}), 400

# LOGOUT
@app.route('/logout', methods=['GET'])
@login_required # Só permite acesso se estiver logado
def logout():

    # Encerra sessão do usuário atual
    logout_user() # remove sessão.
    return jsonify({"menssagem": "Logout realizado com sucesso"})

# CRIAR USUÁRIO (CREATE)
@app.route('/user', methods=['POST'])
def create_user():

    # Cria novo usuário no banco
    data = request.json
    username = data.get("username") # Extrai dados do JSON.
    password = data.get("password") # ////////////////////

    if username and password:

        # Cria objeto User
        user = User (username=username, password=password, role="user") # role padrão é "user"
        db.session.add(user) # Cria objeto User
        db.session.commit()  # Salva no banco de dados
        return jsonify({"Menssagem": "Usuario cadastrado com sucesso"})

    return jsonify ({"Menssagem": "Dados Invalidos"}), 400

# LER USUÁRIO (READ) 
@app.route('/user/<int:id_user>', methods=['GET']) # <int:id_user> = parâmetro na URL.
@login_required
def read_user(id_user):

    # Busca usuário pelo ID
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify ({"menssagem": "Usuario nao encontrado"}), 400

# ATUALIZAR USUÁRIO (UPDATE)
@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):

    # Atualiza senha do usuário
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify ({"Menssagem": "Atualizacao nao permitida"}), 403
    
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()

        return jsonify ({"Menssagem": f"Usuario {id_user} atualizado com sucesso"})
    
    return jsonify ({"menssagem": "Usuario nao encontrado"}), 400

# DELETAR USUÁRIO (DELETE)
@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != "admin":
        return jsonify ({"Menssagem": "Delecao nao permitida"}), 403

    # Impede que usuário delete a si mesmo
    if id_user == current_user.id:
        return jsonify ({"Menssagem": "Delecao nao permitida"}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"Menssagem": f"Usuario {id_user} deletado com sucesso"})
    
    return jsonify ({"menssagem": "Usuario nao encontrado"}), 400



# verifica se esta sendo executado 
if __name__ == "__main__":
    app.run(debug=True)