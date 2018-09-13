from pxa import db
from pxa.models.website import Website
from tests.base import BaseTestCase


class TestModelWebsite(BaseTestCase):

    def test_create_website(self):
        website = Website()
        website.url = 'http://ibm.com.br'
        website.status = Website.Status.NEW
        db.session.add(website)
        db.session.commit()

        self.assertEqual(Website.query.count(), 1)

    def test_validate_url(self):
        website = Website()

        with self.assertRaisesRegexp(ValueError, "Url need be string"):
            website.url = 0

        with self.assertRaisesRegexp(ValueError, "Url need be a valid url"):
            website.url = ''

        website.url = 'http://ibm.com.br'
        self.assertEqual(website.url, 'http://ibm.com.br')

    def test_validate_status(self):
        website = Website()

        with self.assertRaisesRegexp(ValueError, "Invalid Status"):
            website.status = "example"

        website.status = Website.Status.NEW
        self.assertEqual(website.status, Website.Status.NEW)
