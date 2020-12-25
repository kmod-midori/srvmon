from flask_security import auth_required, current_user
from flask import request
from . import api_bp, render_paginated
from . import validator as validators
from ..db import db, Record
from ..utils import render_json_ok, render_json_err


@api_bp.route('/servers/<int:server_id>/records', methods=['GET'])
@auth_required()
def get_records(server_id):
    validator = validators.with_paging({})
    params = validator.validated(dict(request.args))
    if not params:
        return render_json_err("Validation failed", validator.errors)

    query = Record.query.filter_by(server_id=server_id)
    return render_paginated(query, params)