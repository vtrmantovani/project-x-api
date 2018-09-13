import unittest

from pxa import create_app


class BaseTestCase(unittest.TestCase):

    def create_app(self):
        app = create_app('Testing')
        app.app_context().push()
        return app

    def setUp(self):
        """
        Before each test, set up a blank database
        """
        self.app = self.create_app()
        self.client = self.app.test_client()

        self.load_fixtures()

    def load_fixtures(self):
        pass
