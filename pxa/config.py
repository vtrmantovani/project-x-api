import logging
import os


class BaseConfig(object):
    DEBUG = False
    LOGS_LEVEL = logging.INFO
    SQLALCHEMY_DATABASE_URI = os.environ.get('PXA_DB_URI', 'sqlite:///:memory:')  # noqa
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/pxa'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = logging.ERROR
