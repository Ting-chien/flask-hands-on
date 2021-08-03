import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.db import get_db

def create_app():

    # build app configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    # init db
    from . import db
    db.init_app(app)
    # test db connection
    @app.route('/create_db')
    def create_db():
        get_db()
        return 'Create db'

    # auth routes
    from app.views import auth
    app.register_blueprint(auth.bp)

    return app