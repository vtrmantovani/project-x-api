from functools import wraps

from flask import current_app, g, request
from itsdangerous import BadSignature
from werkzeug.exceptions import Unauthorized


def requires_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if not auth:
            raise Unauthorized("Authorization API key required")

        auth = auth.split()

        if auth[0] != 'PXaLogin':
            raise Unauthorized('Invalid authorization scheme')

        auth_params = dict([a.strip(',').split('=', 1) for a in auth[1:]])

        apikey = auth_params.get('apikey', '').strip('"')
        if not apikey:
            raise Unauthorized("API key required")

        try:
            profile = current_app.signer.unsign(apikey)
        except BadSignature:
            raise Unauthorized("Invalid API key")

        g.profile = profile
        g.apikey = apikey

        return f(*args, **kwargs)

    return decorated
