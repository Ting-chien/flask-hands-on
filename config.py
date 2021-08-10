import os
from decouple import AutoConfig

config = AutoConfig(search_path=os.getcwd())

class Config(object):
    
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # SECRECT_KEY
    SECRET_KEY = config('SECRET_KEY', default='default')
    # SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'instance/db.sqlite3')
    # SQLALCHEMY_TRACK_MODIFICATIONS
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TEMPLATES_AUTO_RELOAD
    TEMPLATES_AUTO_RELOAD = True
    # DEFAULT_LANGUAGE
    DEFAULT_LANGUAGE = 'en'
    # SUPPORTED_LANGUAGES
    SUPPORTED_LANGUAGES = ['en', 'zh_TW', 'zh_CN']

class DevConfig(Config):

    DEBUG = True

    # SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DEV_DB_ENGINE', default='mysql+pymysql'),
        config('DEV_DB_USERNAME', default='root'),
        config('DEV_DB_PASS', default='r41021210'),
        config('DEV_DB_HOST', default='127.0.0.1'),
        config('DEV_DB_PORT', default=3306),
        config('DEV_DB_NAME', default='test')
    )
    # SQLALCHEMY_ENGINE_OPTIONS
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 7200,
        'pool_timeout': 100,
        'pool_size': 300,
        'max_overflow': 10,
    }

class ProdConfig(Config):
    # SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('PROD_DB_ENGINE'),
        config('PROD_DB_USERNAME'),
        config('PROD_DB_PASS'),
        config('PROD_DB_HOST'),
        config('PROD_DB_PORT'),
        config('PROD_DB_NAME')
    )
    # SQLALCHEMY_ENGINE_OPTIONS
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 7200,
        'pool_timeout': 100,
        'pool_size': 300,
        'max_overflow': 10,
    }

config = {
    'development': DevConfig,
    'default': DevConfig,
    'production': ProdConfig
}