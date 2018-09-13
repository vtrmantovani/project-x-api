import logging


class BaseConfig(object):
    DEBUG = False
    LOGS_LEVEL = logging.INFO


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = logging.ERROR
