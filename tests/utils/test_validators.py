from parameterized import parameterized

from pxa.utils.validators import is_valid_url
from tests.base import BaseTestCase


class TestValidators(BaseTestCase):

    @parameterized.expand([
        ('http://ibm.com.br', True),
        ('https://ibm.com.br', True),
        ('http://i', False),
        ('https://i', False),
        ('ibm.com.br', False),
    ], testcase_func_name=BaseTestCase.custom_name_func)
    def test_is_valid_url(self, value, expected):
        self.assertEquals(is_valid_url(value), expected)

    def test_is_valid_url_withou_string_parm(self):
        with self.assertRaisesRegexp(ValueError, "Url need be string"):
            is_valid_url(0)
