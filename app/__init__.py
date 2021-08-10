import os

from flask import Flask, g, request
from flask_bootstrap import Bootstrap
from flask_babel import Babel

babel = Babel()

def create_app(config):

    # build app configuration
    app = Flask(__name__)
    app.config.from_object(config)
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

    # init babel
    from . import i18n
    i18n.init_app(app)

    # auth routes
    from .views import auth
    app.register_blueprint(auth.bp)

    # users routes
    from .views import users
    app.register_blueprint(users.bp)
    app.add_url_rule('/', endpoint='index')

    return app