# Desafio API Wishlist

## Descrição:

Este projeto se refere a uma API para cadastro e gestão de produtos de uma lista de desejos, os produtos possuem um nome, uma descrição, um link para acessar a página do produto na web, um link para acessar a foto do produto e uma variável "bought" que informa se o produto foi comprado. Para realizar alterações(PUT, POST e DELETE) é necessário autenticar o usuário na API, para realizar consultas(GET) não.

A API também conta com um sistema simples de criação e exclusão de usuário, login e logout.

## Endpoints:

Para essa pequena API foram criados os seguintes endpoints:

| Endpoint               | Função                    | Método  | JSON/Parametros                                                               |
|------------------------|---------------------------|---------|--------------------------------------------------------------------|
|/produtos/     | Retorna todos os produtos         | GET    |                |
|/produto/<int:product_id>         | Retorna o produto conforme o ID informado  | GET     |           |
|/produto/<int:product_id>         | Altera o produto do ID informado, é necessário passar apenas o valor a ser alterado  | PUT     |  {
            "product": "product",
            "description": "description",
            "link": "link",
            "photo": "photo"
        }         |
|/produto/<int:product_id>         | Deleta um produto pelo ID informado  | DELETE     |          |
|/produto/    | Adiciona um novo produto, por padrão a variavel Bought é falsa         | POST    |  {
            "product": "product",
            "description": "description",
            "link": "link",
            "photo": "photo"
        }     |

|/produto/random/    | Retorna um produto aleatório         | GET    |         |
|/comprei/<int:product_id>     | Altera a variável "bought" para True, mostrando que o produto foi comprado        | PUT|               |
|/usuarios/<int:user_id>     | Retorna o ID e login de um usuário  | GET    |               |
|/usuarios/<int:user_id>     | Exclui o usuário do ID informado  | DELETE    |               |
|/cadastro/     | cadastra um novo usuário        | POST    |  {'login': 'login', 'senha':'senha'}             |
|/login/     | Autentica o usuário no sistema        | 
POST   | {'login': 'login', 'senha':'senha'}              |
|/logout/     | Realiza o Logout do usuário         | POST    |               |

