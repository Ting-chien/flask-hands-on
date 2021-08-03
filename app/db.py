from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    db_user_post = db.relationship("Post", backref="post")

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Post(db.Model):
    __tablenme__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(255), nullable=False)

    def __init__(self, author_id, title, body):
        self.author_id = author_id
        self.title = title
        self.body = body

def get_db():
    if 'db' not in g:
        db.create_all()
        g.db = db

    return g.db

def init_app(app):
    db.init_app(app)