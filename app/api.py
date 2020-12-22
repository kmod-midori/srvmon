from flask import Blueprint, render_template, abort, jsonify, make_response, request
from flask_security import auth_required, current_user
from werkzeug.datastructures import MultiDict

from .db import db, Server
from .utils import render_json_ok, render_json_err
from . import validator as validators

api_bp = Blueprint('api', __name__)


@api_bp.route('/accounts/current')
@auth_required()
def current_account():
    return render_json_ok(id=current_user.id, email=current_user.email)


@api_bp.route('/servers', methods=['PUT'])
@auth_required()
def add_server():
    validator = validators.server_validator()
    data = validator.validated(request.get_json())
    if data:
        config = data['config']
        config['timeout'] = data['timeout']
        server = Server(label=data['label'], mode=data['mode'], enabled=True)
        server.set_config(config)
        db.session.add(server)
        db.session.commit()
        return render_json_ok(id=server.id)

    return render_json_err("Validation failed", validator.errors)
