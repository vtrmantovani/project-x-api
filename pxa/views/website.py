from elasticsearch.exceptions import ElasticsearchException
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from pxa import db, logger
from pxa.models.no_sql.website import WebsiteNoSql
from pxa.models.website import Website
from pxa.utils.api_exceptions import BadRequestGeneric
from pxa.utils.decorators import (requires_api_key, requires_fields_validation,
                                  requires_json)

bp_website = Blueprint('website', __name__, url_prefix='/api')


@requires_api_key
@requires_json
@requires_fields_validation
@bp_website.route('/website', methods=['POST'])
def create():
    r = request.json
    website = Website()
    website.url = r['url']
    website.status = Website.Status.NEW
    try:
        db.session.add(website)
        db.session.commit()
    except SQLAlchemyError as e:
        logger.error("SQLAlchemyError error in create website: {0}".format(e))
        raise BadRequestGeneric(description="Some problems in bd")
    return jsonify(), 201


@requires_api_key
@bp_website.route('/website/<p_website_id>', methods=['GET'])
def get(p_website_id):
    try:
        website_db = WebsiteNoSql()
        website = website_db.get(p_website_id)
        if not website:
            raise NotFound("Website id not found")

        urls = website['_source']
        if not urls:
            logger.error("Source not found on website_id={}".format(p_website_id))  # noqa
            raise BadRequestGeneric(description="Source not found")
    except ElasticsearchException as e:
        logger.error("ElasticsearchException error in get website_id:{0}. Error:{1}".format(p_website_id, e))  # noqa
        raise BadRequestGeneric(description="Some problems in bd")

    return jsonify(website['_source'])
