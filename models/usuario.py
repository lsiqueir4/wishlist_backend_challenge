from sql_alchemy import banco

#configuração da tabela usuarios no DB
class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key = True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    # Converter dados para json
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    #Metodo para buscar pelo ID
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    #Metodo para buscar pelo login
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    #Metodo para salvar login no banco
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
    
    #Metodo para excluir login
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
