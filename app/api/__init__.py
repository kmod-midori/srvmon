from flask import Blueprint
from werkzeug.exceptions import HTTPException

import json

from ..utils import render_json_ok

api_bp = Blueprint('api', __name__)


def render_paginated(query, params, marshal_item=None):
    per_page = params['itemsPerPage']
    if per_page <= 0:
        per_page = 10
    pg = query.paginate(page=params['page'],
                        per_page=per_page,
                        error_out=False)
    if not marshal_item:
        marshal_item = lambda x: x.to_dict()
    return render_json_ok(items=list(map(marshal_item, pg.items)),
                          pages=pg.pages,
                          total=pg.total)


@api_bp.errorhandler(HTTPException)
def handle_exc(e):
    response = e.get_response()
    response.data = json.dumps({
        'meta': {
            'code': e.code
        },
        'payload': {
            'error': e.name + ": " + e.description
        }
    })
    response.content_type = "application/json"
    return response


from . import server, contact, record, account, home