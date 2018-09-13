import json

from tests.base import BaseTestCase


class TestViewCommonCase(BaseTestCase):

    def setUp(self):
        super(TestViewCommonCase, self).setUp()

    def test_healthcheck(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(r['service'], "Project X API")
