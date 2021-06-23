import os


class DevelopConfig:
    SECRET_KEY = 'blabla'
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'marcin16661@gmail.com'
    MAIL_PASSWORD = 'nwkiksbmzyhfvnyc'
