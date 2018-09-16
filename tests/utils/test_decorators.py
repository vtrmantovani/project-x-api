import json

from flask import request

from pxa.utils.api_exceptions import BadRequestGeneric
from pxa.utils.decorators import (requires_api_key, requires_fields_validation,
                                  requires_json)
from tests.base import BaseTestCase


class TestDecoratorsCase(BaseTestCase):

    def setUp(self):
        super(TestDecoratorsCase, self).setUp()
        self.auth_header = 'PXaLogin apikey="test.DU4jJQ.o8vOA378DsITlFQx1etXqt3c-8Q"'  # noqa

        @self.app.route('/api_key_required', methods=['GET'])
        @requires_api_key
        def api_key_required():
            return 'OK'

        @self.app.route('/json_required', methods=['POST'])
        @requires_json
        def json_required():
            return 'OK'

        @self.app.route('/requires_fields_validation', methods=['POST'])
        @requires_fields_validation
        def fields_validation():
            r = request.json
            field1 = r["field1"]  # required
            field2 = r.get("field2")  # optional  # noqa
            if field1 != "value1":
                raise BadRequestGeneric("Invalid value for field1")
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

    def test_requires_json(self):
        response = self.client.post("/json_required",
                                    headers={"content-type": "application/json"})  # noqa
        self.assertEqual(response.status_code, 200)

    def test_requires_json_fail(self):
        response = self.client.post("/json_required")
        self.assertEqual(response.status_code, 415)

    def test_requires_fields_validation(self):
        response = self.client.post("/requires_fields_validation",
                                    headers={"content-type": "application/json"},  # noqa
                                    data=json.dumps({"field1": "value1", "field2": "value2"}))  # noqa
        self.assertEqual(response.status_code, 200)

    def test_requires_fields_validation_optional_param(self):
        response = self.client.post("/requires_fields_validation",
                                    headers={"content-type": "application/json"},  # noqa
                                    data=json.dumps({"field1": "value1"}))  # noqa
        self.assertEqual(response.status_code, 200)

    def test_requires_fields_validation_fail_value(self):
        response = self.client.post("/requires_fields_validation",
                                    headers={"content-type": "application/json"},  # noqa
                                    data=json.dumps({"field1": "invalid"}))  # noqa
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid value for field1", str(response.data))

    def test_requires_fields_validation_fail_field_required(self):
        response = self.client.post("/requires_fields_validation",
                                    headers={"content-type": "application/json"},  # noqa
                                    data=json.dumps({"field2": "value2"}))  # noqa
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing parameter", str(response.data))
