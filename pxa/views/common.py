from flask import Blueprint, jsonify

bp_common = Blueprint('common', __name__, url_prefix='/')


@bp_common.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"service": "Project X API", "version": "0.0.1"})
