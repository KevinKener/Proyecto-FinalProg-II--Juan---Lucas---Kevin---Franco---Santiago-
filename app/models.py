# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Crea la instancia de SQLAlchemy aquí

class Juego(db.Model):
    __tablename__ = 'juegos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    categoria = db.Column(db.String(50))
    anio_lanzamiento = db.Column(db.Integer)
    foto = db.Column(db.String(100))
