from flask_security import auth_required, current_user
from flask import request
from datetime import datetime
from . import api_bp, render_paginated
from . import validator as validators
from ..db import db, Server, User, transaction
from ..utils import render_json_ok, render_json_err


@api_bp.route('/servers', methods=['PUT'])
@auth_required()
def add_server():
    validator = validators.server_validator()
    data = validator.validated(request.get_json())
    if not data: return render_json_err("Validation failed", validator.errors)
    config = data['config']
    with transaction():
        user = User.query.get_or_404(current_user.id)
        server = Server(label=data['label'],
                        mode=data['mode'],
                        enabled=data['enabled'])
        server.set_config(config)
        server.users.append(user)
        db.session.add(server)

    return render_json_ok(id=server.id)


@api_bp.route('/servers', methods=['GET'])
@auth_required()
def get_servers():
    validator = validators.with_paging({
        'enabled': {
            'type': 'boolean',
            'coerce': (str, validators.to_bool)
        },
        'with_status': {
            'type': 'boolean',
            'coerce': (str, validators.to_bool),
            'default': False
        }
    })
    params = validator.validated(dict(request.args))
    if not params:
        return render_json_err("Validation failed", validator.errors)

    query = Server.query
    if 'enabled' in params:
        query = query.filter_by(enabled=params['enabled'])
    if params['with_status']:
        return render_paginated(query, params, lambda s: s.to_dict_ext())
    else:
        return render_paginated(query, params)


@api_bp.route('/servers/<int:server_id>', methods=['GET'])
@auth_required()
def get_server(server_id):
    server = Server.query.get_or_404(server_id)
    server_dic = server.to_dict()
    users = server.users
    server_dic['watching'] = False
    for user in users:
        if user.id == current_user.id:
            server_dic['watching'] = True
    return render_json_ok(**server_dic)


@api_bp.route('/servers/<int:server_id>', methods=['POST'])
@auth_required()
def update_server(server_id):
    validator = validators.server_validator(False)
    data = validator.validated(request.get_json())
    if not data: return render_json_err("Validation failed", validator.errors)
    
    with transaction():
        server = Server.query.get_or_404(server_id)
        if 'label' in data:
            server.label = data['label']
        if 'mode' in data:
            server.mode = data['mode']
        if 'enabled' in data:
            server.enabled = data['enabled']
        if 'config' in data:
            server.set_config(data['config'])
    return render_json_ok(**server.to_dict())


@api_bp.route('/servers/<int:server_id>', methods=['DELETE'])
@auth_required()
def delete_server(server_id):
    with transaction():
        server = Server.query.get_or_404(server_id)
        db.session.delete(server)
    return render_json_ok(id=server_id)

@api_bp.route('/servers/<int:server_id>/watch', methods=['PUT'])
@auth_required()
def watch_server(server_id):
    with transaction():
        user = User.query.get_or_404(current_user.id)
        server = Server.query.get_or_404(server_id)
        server.users.append(user)
    return render_json_ok()

@api_bp.route('/servers/<int:server_id>/watch', methods=['DELETE'])
@auth_required()
def unwatch_server(server_id):
    with transaction():
        user = User.query.get_or_404(current_user.id)
        server = Server.query.get_or_404(server_id)
        server.users.remove(user)
    return render_json_ok()