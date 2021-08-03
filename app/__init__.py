import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_app():

    # build app configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    # init db
    db.init_app(app)
    # create db connect
    @app.route('/create_db')
    def createt_db():
        db.create_all()
        return 'ok'

    # auth routes
    from app.views import auth
    app.register_blueprint(auth.bp)

    return app