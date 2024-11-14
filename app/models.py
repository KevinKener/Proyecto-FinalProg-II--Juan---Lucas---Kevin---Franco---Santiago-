# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Crea la instancia de SQLAlchemy aquí

class Juego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    categoria = db.Column(db.String(100))
    year = db.Column(db.Integer)
    plataforma = db.Column(db.String(100))
    precio = db.Column(db.Float)
    favorito = db.Column(db.Boolean)
    foto = db.Column(db.String(100), nullable=True)
