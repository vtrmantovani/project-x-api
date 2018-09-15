from celery import Celery

from pxa.celery_worker import create_celery
from tests.base import BaseTestCase


class TestCeleryWork(BaseTestCase):

    def test_create_celery(self):
        app = self.create_app()
        result = create_celery(app)
        self.assertTrue(isinstance(result, Celery))
