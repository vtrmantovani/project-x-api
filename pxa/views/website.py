from flask import Blueprint, jsonify, request

from pxa import db
from pxa.models.website import Website
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
    db.session.add(website)
    db.session.commit()

    return jsonify(), 201
