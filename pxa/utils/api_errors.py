from flask import Response, json
from werkzeug.exceptions import HTTPException


def generic_api_error(e):
    if not isinstance(e, HTTPException):
        raise HTTPException

    resp = json.dumps({"error": {"status": e.code,
                                 "title": e.name,
                                 "code": getattr(e, 'api_code', 'UNDEFINED'),
                                 "message": e.description
                                 }})
    response = Response(resp, status=e.code, mimetype='application/json')
    response.cache_control.private = True
    response.cache_control.must_revalidate = True
    return response


def install_error_handlers(error_codes, blueprint):
    for code in error_codes:
        blueprint.errorhandler(code)(generic_api_error)
