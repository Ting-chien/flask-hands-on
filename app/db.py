from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(155), nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

def get_db():
    if 'db' not in g:
        db.create_all()
        g.db = db

    return g.db

def init_app(app):
    db.init_app(app)