import json

from pxa.models.website import Website
from tests.base import BaseTestCase


class TestViewWebsite(BaseTestCase):

    def setUp(self):
        self.api_key = 'PXaLogin apikey="test.DU4jJQ.o8vOA378DsITlFQx1etXqt3c-8Q"'  # noqa
        super(TestViewWebsite, self).setUp()
        self.app.test_request_context().push()

    def test_create_website(self):
        params = {
            "url": "http://vtrmantovani.com.br",
        }
        response = self.client.post("/api/website", headers={
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }, data=json.dumps(params))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Website.query.count(), 1)
