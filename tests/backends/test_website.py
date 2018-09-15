import vcr
from parameterized import parameterized

from pxa import db
from pxa.backends.exceptions import WebsiteBackendException
from pxa.backends.website import WebsiteBackend
from pxa.models.website import Website
from tests.base import BaseTestCase


class TestBackendWebsite(BaseTestCase):

    def setUp(self):
        super(TestBackendWebsite, self).setUp()

    def load_fixtures(self):
        website = Website()
        website.url = "http://vtrmantovani.com.br"
        website.status = Website.Status.NEW

        self.website = website

    def test_get_available_links(self):
        db.session.add(self.website)
        db.session.commit()

        self.assertEqual(Website.query.count(), 1)

        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links.yaml'):  # noqa
            website_backend = WebsiteBackend()
            list_urls = website_backend._get_available_links(self.website)

        self.assertEquals(list_urls[0], 'https://github.com/vtrmantovani')
        self.assertEquals(list_urls[1], 'https://www.linkedin.com/in/vtrmantovani')  # noqa
        self.assertEqual(Website.query.count(), 3)

    def test_save_website(self):
        website_backend = WebsiteBackend()
        website_backend._save_website("http://vtrmantovani.com.br")

        self.assertEqual(Website.query.count(), 1)

    def test_get_available_links_without_urls(self):
        db.session.add(self.website)
        db.session.commit()

        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links_without_urls.yaml'):  # noqa
            website_backend = WebsiteBackend()
            list_urls = website_backend._get_available_links(self.website)

        self.assertEquals(list_urls, [])
        self.assertEqual(Website.query.count(), 1)

    def test_get_available_links_without_status_200(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links_without_status_200.yaml'):  # noqa
            self.website.url = 'http://vtrmantovani.com.br/not-found'

            with self.assertRaises(WebsiteBackendException) as error:
                website_backend = WebsiteBackend()
                website_backend._get_available_links(self.website)

            self.assertEqual(str(error.exception),   "Response status code not is 200")  # noqa

    def test_get_available_links_without_response_text(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links_without_response_text.yaml'):  # noqa

            with self.assertRaises(WebsiteBackendException) as error:
                website_backend = WebsiteBackend()
                website_backend._get_available_links(self.website)

            self.assertEqual(str(error.exception),  "Response text without value")  # noqa

    def test_get_available_links_with_connection_error(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links_with_connection_error.yaml'):  # noqa
            self.website.url = 'http://a.com'

            with self.assertRaises(WebsiteBackendException) as error:
                website_backend = WebsiteBackend()
                website_backend._get_available_links(self.website)

            self.assertEqual(str(error.exception),  "ConnectionError on request")  # noqa

    def test_save_website_available_links(self):
        db.session.add(self.website)
        db.session.commit()

        self.assertEqual(Website.query.count(), 1)

        with vcr.use_cassette('tests/fixtures/cassettes/test_save_website_available_links.yaml'):  # noqa
            website_backend = WebsiteBackend()
            website_backend.save_website_available_links(self.website)

        website_db = Website.query.filter(Website.id == 1).first()  # noqa

        self.assertEqual(website_db.status.value, "DONE")
        self.assertEqual(Website.query.count(), 3)

    def test_failed_save_website_available_links(self):
        db.session.add(self.website)
        db.session.commit()

        website_backend = WebsiteBackend()
        website_backend.failed_save_website_available_links(self.website, 'Error')  # noqa

        website_db = Website.query.filter(Website.id == 1).first()  # noqa
        self.assertEqual(Website.query.count(), 1)
        self.assertEqual(website_db.status.value, 'ERROR')
        self.assertEqual(website_db.status_desc, 'Error')  # noqa

    @parameterized.expand([
        ("http://vtrmantovani.com.br", True),
        ("http://ibm.com.br", False),
    ], testcase_func_name=BaseTestCase.custom_name_func)
    def test_check_if_website_exist(self, value, expected):
        db.session.add(self.website)
        db.session.commit()
        website_backend = WebsiteBackend()
        self.assertEquals(website_backend._check_if_website_exist(value), expected)  # noqa
