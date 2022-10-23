import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


class DevelopConfig(Config):
    DEBUG = os.environ.get('DEBUG')
    MAIL_SERVER = 'smtp'
    MAIL_PORT = 2500
    MAIL_USE_TLS = False


class ProductionConfig(Config):
    DEBUG = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'secret_key'
    WTF_CSRF_ENABLED = False
    WTF_CSRF_METHODS = []
    LOGIN_DISABLED = False
