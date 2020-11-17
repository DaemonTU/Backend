from os import path,environ
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR,'.env'))

class Config:
    SECRET_KEY= environ.get('SECRET_KEY')
    TESTING = False
class Development(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    MONGO_URI = environ.get('DEV_DATABASE_URI')
class Production(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    MONGO_URI = environ.get('PROD_DATABASE_URI')
