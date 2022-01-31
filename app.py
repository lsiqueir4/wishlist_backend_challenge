from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.product import Product, Products, Add_Product, Bought_Product, Random_Product
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from sql_alchemy import banco

#Configurações de conexao com banco de dados e lib de autenticacao
db_connect_local = "postgresql://postgres:1234@localhost:5432/postgres"
db_connect = "postgres://nizrfeqjpidhdn:2a316ae1a179ba06c88b94482f174fcd5cc206cb9ae47f6494f6b22426ed5a2d@ec2-54-208-139-247.compute-1.amazonaws.com:5432/d17stcussq14qu"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connect
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)

jwt = JWTManager(app)


@app.route('/')
def index():
    return '<h1>Bem-vindo a Api de Wishlist</h1>'

#Garante que o banco seja criado 
@app.before_first_request
def cria_banco():
    banco.create_all()

#Leitura da Blacklist
@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

#Quando usuário na blacklist(fez logout), retorna mensagem
@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been Logged out'}), 401

api.add_resource(Products, '/produtos/')
api.add_resource(Product, '/produto/<int:product_id>')
api.add_resource(Add_Product, '/produto/')
api.add_resource(Random_Product, '/produto/random/')
api.add_resource(Bought_Product, '/comprei/<int:product_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro/')
api.add_resource(UserLogin, '/login/')
api.add_resource(UserLogout, '/logout/')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)