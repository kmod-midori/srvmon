from flask_security import auth_required, current_user
from . import api_bp
from ..utils import render_json_ok
from ..db import db, User


@api_bp.route('/accounts/current')
@auth_required()
def current_account():
    return render_json_ok(id=current_user.id, email=current_user.email)


@api_bp.route('/accounts')
@auth_required()
def all_accounts():
    users = User.query.all()
    users = list(map(lambda x: x.to_dict(), users))
    return render_json_ok(users=users)