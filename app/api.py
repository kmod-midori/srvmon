from flask import Blueprint, render_template, abort, jsonify, make_response
from flask_security import auth_required, current_user

from .db import db
from .utils import render_json_ok, render_json_err

api_bp = Blueprint('api', __name__)


@api_bp.route('/accounts/current')
@auth_required()
def current_account():
    return render_json_ok(id=current_user.id, email=current_user.email)
