import logging
import os
import sys
from flask import Flask
from pxa.utils.api_errors import install_error_handlers
logger = logging.getLogger(__name__)


def configure_logger(app):
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(app.config['LOGS_LEVEL'])
        logger.addHandler(ch)


def create_app(config_var=os.getenv('DEPLOY_ENV', 'Development')):
    # init application
    app = Flask(__name__)
    app.config.from_object('pxa.config.%sConfig' % config_var)

    # configure logger
    configure_logger(app)

    # register Blueprints
    from pxa.views.common import bp_common
    app.register_blueprint(bp_common)

    # install error handler for views
    error_codes = [400, 401, 403, 404, 405, 406, 408, 409, 410, 412, 415, 428,
                   429, 500, 501]

    install_error_handlers(error_codes, app)
    return app
