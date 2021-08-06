import os

from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():

    # build app configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    bootstrap = Bootstrap(app)

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

    # auth routes
    from app.views import auth
    app.register_blueprint(auth.bp)

    # users routes
    from app.views import users
    app.register_blueprint(users.bp)
    app.add_url_rule('/', endpoint='index')

    return app