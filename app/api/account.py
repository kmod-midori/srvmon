from flask_security import auth_required, current_user
from . import api_bp
from ..utils import render_json_ok


@api_bp.route('/accounts/current')
@auth_required()
def current_account():
    return render_json_ok(id=current_user.id, email=current_user.email)