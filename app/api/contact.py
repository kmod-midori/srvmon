from flask_security import auth_required, current_user
from flask import Blueprint, render_template, abort, jsonify, make_response, request
from . import api_bp, render_paginated
from . import validator as validators
from ..db import db, Contact
from ..utils import render_json_ok, render_json_err

@api_bp.route('/contacts', methods=['PUT'])
@auth_required()
def add_contact():
    pass

@api_bp.route('/contacts', methods=['GET'])
@auth_required()
def get_contacts():
    validator = validators.with_paging({})
    params = validator.validated(dict(request.args))
    if not params:
        return render_json_err("Validation failed", validator.errors)

    query = Contact.query.filter_by(user_id=current_user.id)
    return render_paginated(query, params)