from flask import Flask, request , jsonify # Importação da biblioteca Flask
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__) # cria aplicação
app.config['SECRET_KEY'] = "sua_chave_secreta" # 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # caminho para conexao do banco

login_Manager = LoginManager()
db.init_app(app)
login_Manager.init_app(app)

login_Manager.login_view = 'login'

# cria rota
@app.route('/login', methods=['POST'])
def login(user):
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        #login
        user = User.query.filter_by(username=username).first()

# funcao de verificacao se a senha esta correta 
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"Menssagem": "Autencicação realizada com sucesso"})
    
    return jsonify({"Menssagem": "Credenciais Invalida"}), 400


@app.route("/")
def home():
    return "Página inicial"

@app.route("/hello-world", methods = ["GET"])
def hello_word():
    return "Hello World"

# verifica se esta sendo executado 
if __name__ == '_main_':
    app.run(debug=True)