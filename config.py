import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ngle_api_tongchun')
    DEBUG = False


class LocalConfig(Config):
    DEBUG = True
    DATABASE_URI = 'mongodb://localhost:27017'


class DevConfig(Config):
    DEBUG = True
    DATABASE_URI = 'mongodb://mongodb:27017'


class ProdConfig(Config):
    DEBUG = False
    DATABASE_URI = 'mongodb://mongodb:27017'


config_by_name = dict(dev=DevConfig, local=LocalConfig, prod=ProdConfig)

key = Config.SECRET_KEY
