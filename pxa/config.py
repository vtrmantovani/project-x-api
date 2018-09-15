import logging
import os

from kombu import Exchange, Queue


class BaseConfig(object):
    DEBUG = False
    LOGS_LEVEL = logging.INFO
    SQLALCHEMY_DATABASE_URI = os.environ.get('PXA_DB_URI', 'sqlite:///:memory:')  # noqa
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECONDS = 60
    MINUTES = SECONDS * 60
    TIMEOUT_WEBSITE = int(os.environ.get('TIMEOUT_WEBSITE', 1 * MINUTES))

    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', 'localhost:9200')  # noqa

    BROKER_URL = os.environ.get('BROKER_URL')  # noqa
    CELERY_IGNORE_RESULT = True
    CELERY_RESULT_BACKEND = BROKER_URL
    CELERY_QUEUES = (
        Queue('pxa.website',
              Exchange('pxa.website'),
              routing_key='pxa.website'),
        )


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/pxa'
    BROKER_URL = 'redis://localhost:6379/0'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = logging.ERROR
