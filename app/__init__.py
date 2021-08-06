import os

from flask import Flask, g, request
from flask_bootstrap import Bootstrap
from flask_babel import Babel

babel = Babel()

def create_app():

    # build app configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEFAULT_LANGUAGE'] = 'en'
    app.config['SUPPORTED_LANGUAGES'] = ['en', 'zh_TW', 'zh_CN']
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
    babel.init_app(app)
    register_i18n(app)

    # auth routes
    from .views import auth
    app.register_blueprint(auth.bp)

    # users routes
    from .views import users
    app.register_blueprint(users.bp)
    app.add_url_rule('/', endpoint='index')

    return app

def register_i18n(app):
    """Register i18n with the Flask application."""
    defalut_language_str = app.config['DEFAULT_LANGUAGE']
    support_language_list = app.config['SUPPORTED_LANGUAGES']

    # 1 Get parameter lang_code from route
    @app.url_value_preprocessor
    def get_lang_code(endpoint, values):
        if values is not None:
            g.lang_code = values.pop('lang_code', defalut_language_str)

    # 2 Check lang_code type is in config
    @app.before_request
    def ensure_lang_support():
        lang_code = g.get('lang_code', None)
        if lang_code and lang_code not in support_language_list:
            g.lang_code = request.accept_languages.best_match(support_language_list)

    # 3 Setting babel
    @babel.localeselector
    def get_locale():
        return g.get('lang_code')

    # 4 Check lang_code exist after step1 pop parameter of lang_code
    @app.url_defaults
    def set_language_code(endpoint, values):
        if 'lang_code' in values or not g.lang_code:
            return
        if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
            values['lang_code'] = g.lang_code