from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # definicao do usuario: id (int), username (text), password(tetx), role (text)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True) # cria usuario com nome unico
    password = db.Column(db.String(80), nullable=False) # cria senha
    role = db.Column(db.String(80), nullable=False, default="user") # define papel do usuario (admin ou user)
