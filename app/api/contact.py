from flask_security import auth_required, current_user
from flask import Blueprint, render_template, abort, jsonify, make_response, request
from . import api_bp, render_paginated
from . import validator as validators
from ..db import db, Contact, transaction
from ..utils import render_json_ok, render_json_err
from . import validator as validators


@api_bp.route('/contacts', methods=['PUT'])
@auth_required()
def add_contact():
    validator = validators.contact_validator()
    data = validator.validated(request.get_json())
    if not data: return render_json_err("Validation failed", validator.errors)
    config = data['config']
    with transaction():
        contact = Contact(user_id=current_user.id,
                          type=data['type'],
                          enabled=data['enabled'])
        contact.set_config(config)
        db.session.add(contact)
    return render_json_ok(id=contact.id)


@api_bp.route('/contacts', methods=['GET'])
@auth_required()
def get_contacts():
    validator = validators.with_paging({})
    params = validator.validated(dict(request.args))
    if not params:
        return render_json_err("Validation failed", validator.errors)

    query = Contact.query.filter_by(user_id=current_user.id)
    contacts = list(map(lambda x: x.to_dict(), query.all()))
    return render_json_ok(contacts=contacts)


@api_bp.route('/contacts/<int:contact_id>', methods=['POST'])
@auth_required()
def update_contact(contact_id):
    validator = validators.contact_validator(False)
    data = validator.validated(request.get_json())
    if not data: return render_json_err("Validation failed", validator.errors)

    with transaction():
        contact = Contact.query.filter_by(
            id=contact_id, user_id=current_user.id).first_or_404()

        if 'type' in data:
            contact.type = data['type']
        if 'enabled' in data:
            contact.enabled = data['enabled']
        if 'config' in data:
            contact.set_config(data['config'])
    return render_json_ok(**contact.to_dict())


@api_bp.route('/contacts/<int:contact_id>', methods=['DELETE'])
@auth_required()
def delete_contact(contact_id):
    with transaction():
        contact = Contact.query.filter_by(
            id=contact_id, user_id=current_user.id).first_or_404()
        db.session.delete(contact)
    return render_json_ok(id=contact_id)
