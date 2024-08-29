import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQL_TRACK_MODIFICATIONS = False
    # another line in pdf here

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
            'mysql+pymysql://vicio_user:010011010@localhost/vicio_dev'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
            'mysql+pymysql://vicio_user:010011010@localhost/vicio_test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or \
            'mysql+pymysql://vicio_user:010011010@localhost/vicio_prod'

config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,

        'default': DevelopmentConfig
        }
