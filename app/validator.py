from cerberus import Validator

server_schema = {
    'label': {
        'type': 'string'
    },
    'timeout': {
        'type': 'integer',
        'min': 1
    },
    'mode': {
        'type': 'string',
        'allowed': ['active-http', 'active-tcp', 'passive-http']
    },
    'config': {
        'type':
        'dict',
        'require_all':
        True,
        'oneof_schema': [{}, {
            'url': {
                'type': 'string'
            },
            'validStatus': {
                'type': 'list',
                'schema': {
                    'type': 'integer',
                    'min': 100,
                    'max': 599
                }
            }
        }, {
            'address': {
                'type': 'string'
            },
            'port': {
                'type': 'integer',
                'min': 1,
                'max': 65535
            }
        }]
    }
}


def server_validator():
    return Validator(server_schema, require_all=True)
