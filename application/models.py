from db import datab
from flask_login import UserMixin

class Usuario(UserMixin, datab.Model):
    __tablename__ = 'usuarios'

    id = datab.Column(datab.Integer,primary_key=True)

    nome = datab.Column(datab.String(35), unique=True)
    senha = datab.Column(datab.String())