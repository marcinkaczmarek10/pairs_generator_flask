import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'in-v3.mailjet.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


class DevelopConfig(Config):
    DEBUG = True
    SECRET_KEY = 'secret_key'


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'secret_key'
    WTF_CSRF_ENABLED = False
    WTF_CSRF_METHODS = []
    LOGIN_DISABLED = False
