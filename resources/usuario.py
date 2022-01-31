from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

#Variavel global argumentos, pega o json passado em um PUT ou POST
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str,required=True, help="the field 'login' cannot be left blank")
atributos.add_argument('senha', type=str,required=True, help="the field 'senha' cannot be left blank")

#GET: Retorna um usuário pelo ID
#DELETE: Exclui um usuário pelo ID
class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found.'}, 404
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {"message": 'An internal error ocurred trying to delete user.'}, 500
            return {'message': 'user deleted.'}
        return {'message': 'user not found.'}, 404

#POST: Cria um novo usuário
class UserRegister(Resource):
    
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": f"the login '{dados['login']}' already exists."}

        user = UserModel(**dados)
        user.save_user()
        return {"message": "User created successfully!"},201

# Autentica o usuário e retorna um token de acesso
class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity = user.user_id)
            return {'acess_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect'}, 401 #unauthorized

#Metodo para logout, adiciona o usuário em uma Blacklist
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out sucessfuly'}