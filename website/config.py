import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'in-v3.mailjet.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'aa9c73e11650019d398cce37006c4255'
    MAIL_PASSWORD = '07b662a0302b24667712a5e36c782884'


class DevelopConfig(Config):
    DEBUG = True
    SECRET_KEY = 'secret_key'


class ProductionConfig(Config):
    DEBUG = False
