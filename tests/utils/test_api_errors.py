import unittest

from flask import Flask, json
from werkzeug.exceptions import Conflict, Forbidden, HTTPException

from pxa.utils.api_errors import generic_api_error, install_error_handlers


class DataErrorException(Conflict):
    api_code = 'DATA_ERROR'


class TestApiErrosCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

        error_codes = [409, 500]
        install_error_handlers(error_codes, self.app)

        @self.app.route('/http_status_409', methods=['POST'])
        def http_status_409():
            raise DataErrorException("A long error description")

        @self.app.route('/http_status_403', methods=['POST'])
        def http_status_200():
            raise Forbidden

        @self.app.route('/http_status_500', methods=['POST'])
        def http_status_500():
            raise Exception('Generic exception')

    def test_http_response_with_api_code(self):
        response = self.client.post("/http_status_409")
        self.assertEqual(response.status_code, 409)

        response = json.loads(response.data)

        self.assertEqual(response['error']['status'], 409)
        self.assertEquals(response['error']['title'], 'Conflict')
        self.assertEquals(response['error']['code'], 'DATA_ERROR')
        self.assertEquals(response['error']['message'], 'A long error description')  # noqa

    def test_http_response_without_api_code(self):
        response = self.client.post("/http_status_403")
        self.assertEqual(response.status_code, 403)

    def test_generic_api_error(self):
        with self.assertRaises(HTTPException):
            generic_api_error("")
