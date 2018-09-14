import re


def is_valid_url(value):
    if not isinstance(value, str):
        raise ValueError("Url need be string")

    regex = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return bool(re.match(regex, value))
