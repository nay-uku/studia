from flask_wtf import FlaskForm
from wtforms import StringField


class Product:
    def __init__(self, id, name, description, price):
        self.__searchable__ = ['name', 'description', 'price']
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return 'id:{0}\nname:{1}\ndescription:{2}\nprice:{3}'.format(self.id, self.name, self.description, self.price)


class SearchForm(FlaskForm):
    q = StringField('Czego szukasz?')
