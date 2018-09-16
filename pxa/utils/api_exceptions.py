from werkzeug.exceptions import BadRequest


class BadRequestGeneric(BadRequest):
    def __init__(self, api_code='UNDEFINED', description='BadRequest'):
        self.api_code = api_code
        self.description = description


class BadRequestMissingParams(BadRequest):
    api_code = "PARAM_MISSING"

    def __init__(self, param_name):
        BadRequest.__init__(self)
        self.description = "Missing parameter: {0}".format(param_name)
