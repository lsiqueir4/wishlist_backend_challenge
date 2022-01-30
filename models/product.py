from sql_alchemy import banco

class ProductModel(banco.Model):
    __tablename__ = 'products'

    product_id = banco.Column(banco.Integer, primary_key = True)
    product = banco.Column(banco.String(150))
    description =  banco.Column(banco.String(250))
    link = banco.Column(banco.String(250))
    photo = banco.Column(banco.String(250))
    bought = banco.Column(banco.Boolean, default=False)

    def __init__(self, product, description, link, photo, bought):
        self.product = product
        self.description = description
        self.link = link
        self.photo = photo

    def json(self):
        return {
            'product_id': self.product_id,
            'product': self.product,
            'description': self.description,
            'link': self.link,
            'photo': self.photo,
            'bought': self.bought
        }

    @classmethod
    def find_product(cls, product_id):
        hotel = cls.query.filter_by(product_id=product_id).first()
        if hotel:
            return hotel
        return None

    def save_product(self):
        banco.session.add(self)
        banco.session.commit()

    def update_product(self, product, description, link, photo, bought):
        self.product = product
        self.description = description
        self.link = link
        self.photo = photo
        self.bought = bought

    def bought_product(self, bought):
        self.bought = bought
    
    def delete_product(self):
        banco.session.delete(self)
        banco.session.commit()
