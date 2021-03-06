import logging
import os
import sys

from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_elasticsearch import FlaskElasticsearch
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimestampSigner

from pxa.utils.api_errors import install_error_handlers

es = FlaskElasticsearch()

celery = Celery()

db = SQLAlchemy(session_options={'autoflush': False})

logger = logging.getLogger(__name__)

migrate = Migrate()


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

    # configure celery
    celery.config_from_object(app.config)

    # configure elasticsearch
    es.init_app(app)

    # init database
    db.init_app(app)
    _module_dir = os.path.dirname(os.path.abspath(__file__))
    migrate.init_app(app, db, directory=os.path.join(_module_dir, '..', 'migrations'))  # noqa

    app.signer = TimestampSigner(app.config['SIGNER_KEY'])

    # register Blueprints
    from pxa.views.common import bp_common
    app.register_blueprint(bp_common)
    from pxa.views.website import bp_website
    app.register_blueprint(bp_website)

    # install error handler for views
    error_codes = [400, 401, 403, 404, 405, 406, 408, 409, 410, 412, 415, 428,
                   429, 500, 501]

    install_error_handlers(error_codes, app)
    return app
