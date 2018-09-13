import unittest

from pxa import create_app, db


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

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.load_fixtures()

    def tearDown(self):
        """Get rid of the database again after each test."""
        with self.app.app_context():
            db.drop_all()
            db.session.rollback()

    def load_fixtures(self):
        pass
