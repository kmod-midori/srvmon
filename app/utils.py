from flask import jsonify, make_response


def render_json(payload, code=200, headers=None):
    if not headers:
        headers = dict()
    headers["Content-Type"] = "application/json"
    payload = dict(meta=dict(code=code), payload=payload)
    return make_response(jsonify(payload), code, headers)


def render_json_ok(**payload):
    return render_json(payload)


def render_json_err(message, errors=None, code=400):
    if not errors:
        errors = {}
    return render_json({'errors': errors, 'error': message}, code)
