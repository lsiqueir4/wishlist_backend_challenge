from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.product import Product, Products, Add_Product, Bought_Product, Random_Product
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from sql_alchemy import banco

#Configurações de conexao com banco de dados e lib de autenticacao
db_connect_local = "postgresql://postgres:1234@localhost:5432/postgres"
db_connect = "postgresql://xzuzgkzcnrklgs:671acf3d1e4dafd5373b91f73fa5d3e3ae9e4034b533c34c4de0ee482950ff0f@ec2-54-157-15-228.compute-1.amazonaws.com:5432/dbeam0g0okjbqh"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connect
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)

jwt = JWTManager(app)

#Garante que o banco seja criado 
@app.before_first_request
def cria_banco():
    banco.create_all()

banco.init_app(app)
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
    app.run()