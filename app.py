from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.product import Product, Products, Add_Product, Bought_Product, Random_Product
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:7112@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)

jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

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