import os

from app import create_app
from config import config
from dotenv import  load_dotenv

ENV = os.getenv('FLASK_ENV')

try:
    app_config = config[ENV]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, ...]')

app = create_app(app_config)