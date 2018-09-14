import mock
import vcr
from requests.exceptions import ConnectTimeout

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
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links.yaml'):  # noqa
            website_backend = WebsiteBackend()
            list_urls = website_backend.get_available_links(self.website)
            self.assertEquals(list_urls[0], 'https://github.com/vtrmantovani')
            self.assertEquals(list_urls[1], 'https://www.linkedin.com/in/vtrmantovani')  # noqa

    def test_get_available_links_without_urls(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links_without_urls.yaml'):  # noqa
            website_backend = WebsiteBackend()
            list_urls = website_backend.get_available_links(self.website)
            self.assertEquals(list_urls, [])

    def test_get_available_links_without_status_200(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links_without_status_200.yaml'):  # noqa
            self.website.url = 'http://vtrmantovani.com.br/not-found'

            with self.assertRaises(WebsiteBackendException) as error:
                website_backend = WebsiteBackend()
                website_backend.get_available_links(self.website)

            self.assertEqual(str(error.exception),   "Response status code not is 200")  # noqa

    def test_get_available_links_without_response_text(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links_without_response_text.yaml'):  # noqa

            with self.assertRaises(WebsiteBackendException) as error:
                website_backend = WebsiteBackend()
                website_backend.get_available_links(self.website)

            self.assertEqual(str(error.exception),  "Response text without value")  # noqa

    @mock.patch('pxa.backends.website.WebsiteBackend._get_response_website')
    def test_get_available_links_with_connect_timeout(self, mock_response):
        mock_response.side_effect = mock.Mock(side_effect=ConnectTimeout())
        with self.assertRaises(ConnectTimeout):
            website_backend = WebsiteBackend()
            website_backend.get_available_links(self.website)

        self.assertEqual(mock_response.call_count, 1)

    def test_get_available_links_with_connection_error(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_available_links_with_connection_error.yaml'):  # noqa
            self.website.url = 'http://a.com'

            with self.assertRaises(WebsiteBackendException) as error:
                website_backend = WebsiteBackend()
                website_backend.get_available_links(self.website)

            self.assertEqual(str(error.exception),  "ConnectionError on request")  # noqa
