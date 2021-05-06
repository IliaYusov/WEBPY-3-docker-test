import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRE_URI') or 'postgresql://docker:docker@localhost:5432/docker'
    SALT = os.environ.get('SALT') or 'my_sJHLHLHKLаваыпuper_s!alt_#4$4344'
    STATIC_FOLDER = os.environ.get('STATIC_FOLDER')
