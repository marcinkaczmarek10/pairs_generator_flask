import os


class DevelopConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
