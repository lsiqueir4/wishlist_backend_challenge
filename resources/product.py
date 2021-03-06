from flask_restful import Resource, reqparse
from models.product import ProductModel
from flask_jwt_extended import jwt_required
import random

#Variavel global argumentos, pega o json passado em um PUT ou POST
argumentos = reqparse.RequestParser()
argumentos.add_argument('product', type=str, required=True, help="the fild 'product' cannot be left blank")
argumentos.add_argument('description')
argumentos.add_argument('link')
argumentos.add_argument('photo')
argumentos.add_argument('bought', type=bool, default=False)

#Executa um for na tabela produtos para buscar todos os produtos cadastrados
class Products(Resource):
    def get(self):
        return {'products': [product.json() for product in ProductModel.query.all()]}

#GET: Busca um produto pelo ID, 
#PUT: Altera um produto pelo ID, 
#DELETE: Exclui um produto pelo ID
class Product(Resource):

    def get(self, product_id):
        product = ProductModel.find_product(product_id)
        if product:
            return product.json()
        return {'message': 'Product not found.'}, 404
    
    @jwt_required()
    def put(self, product_id):
        dados = argumentos.parse_args()
        produto_encontrado = ProductModel.find_product(product_id)
        if produto_encontrado:
            produto_encontrado.update_product(**dados)
            produto_encontrado.save_product()
            return produto_encontrado.json(), 200

        product = ProductModel(product_id, **dados)
        product.save_product()
        return product.json(), 201 
    
    @jwt_required()
    def delete(self, product_id):
        product = ProductModel.find_product(product_id)
        if product:
            try:
                product.delete_product()
            except:
                return {"message": 'An internal error ocurred trying to delete product.'}, 500
            return {'message': 'Product deleted.'}
        return {'message': 'Product not found.'}, 404

#Adiciona um novo produto
class Add_Product(Resource):

    @jwt_required()
    def post(self):
        dados = argumentos.parse_args()

        product = ProductModel(**dados)
        try:
            product.save_product()
        except:
            return {"message": 'An internal error ocurred trying to save product.'}, 500
        return product.json()

#Retorna um produto aleat??rio
class Random_Product(Resource):

    def get(self):
        product_list = [product for product in ProductModel.query.all()]

        product_selected = random.choice(product_list)

        if product_selected:
            return product_selected.json()
        return {'message': 'Product not found.'}, 404

#Pega um produto pelo ID e atualiza a variavel bought para True
class Bought_Product(Resource):

    @jwt_required()
    def put(self, product_id):
        atributos = reqparse.RequestParser()
        atributos.add_argument('bought', type=bool, default=True)
        dados = atributos.parse_args()
        produto_encontrado = ProductModel.find_product(product_id)
        if produto_encontrado:
            produto_encontrado.bought_product(**dados)
            produto_encontrado.save_product()
            return produto_encontrado.json(), 200

        product = ProductModel(product_id, **dados)
        product.save_product()
        return product.json(), 201 