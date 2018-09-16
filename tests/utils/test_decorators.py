import json

from pxa.utils.decorators import requires_api_key
from tests.base import BaseTestCase


class TestDecoratorsCase(BaseTestCase):

    def setUp(self):
        super(TestDecoratorsCase, self).setUp()
        self.auth_header = 'PXaLogin apikey="test.DU4jJQ.o8vOA378DsITlFQx1etXqt3c-8Q"'  # noqa

        @self.app.route('/api_key_required', methods=['GET'])
        @requires_api_key
        def api_key_required():
            return 'OK'

    def test_requires_api_key(self):
        response = self.client.get(
            '/api_key_required',
            headers={'Authorization': self.auth_header}
        )
        self.assertEqual(response.status_code, 200)

    def test_requires_api_key_fail(self):
        response = self.client.get('/api_key_required')
        self.assertEqual(response.status_code, 401)

    def test_requires_api_key_without_api_key(self):
        self.auth_header = 'PXaLogin'
        response = self.client.get(
            '/api_key_required',
            headers={'Authorization': self.auth_header}
        )
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(r['error']['status'], 401)
        self.assertEqual(r['error']['message'], 'API key required')

    def test_requires_api_key_invalid_key_scheme(self):
        response = self.client.get(
            '/api_key_required',
            headers={'Authorization': 'apikey="xpo"'}
        )
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(r['error']['status'], 401)
        self.assertEqual(r['error']['message'], 'Invalid authorization scheme')

    def test_requires_api_key_without_authorization(self):
        response = self.client.get(
            '/api_key_required',
            headers={'Authorization': ''}
        )
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(r['error']['status'], 401)
        self.assertEqual(r['error']['message'], 'Authorization API key required')  # noqa

    def test_requires_api_key_invalid_api(self):
        response = self.client.get(
            '/api_key_required',
            headers={'Authorization': 'PXaLogin apikey="xpo"'}
        )
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(r['error']['status'], 401)
        self.assertEqual(r['error']['message'], 'Invalid API key')
