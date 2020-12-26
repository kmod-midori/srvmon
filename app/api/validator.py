from cerberus import Validator

time_schema = {'type': 'integer', 'min': 1}

server_config_schema = {
    'type':
    'dict',
    'require_all':
    True,
    'anyof_schema': [
        {
            # Passive HTTP
            'interval': time_schema
        },
        {
            # Active HTTP
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
            },
            'timeout': time_schema,
            'interval': time_schema
        },
        {
            # Active TCP
            'address': {
                'type': 'string'
            },
            'port': {
                'type': 'integer',
                'min': 1,
                'max': 65535
            },
            'timeout': time_schema,
            'interval': time_schema
        }
    ]
}

server_schema = {
    'label': {
        'type': 'string'
    },
    'mode': {
        'type': 'string',
        'allowed': ['active-http', 'active-tcp', 'passive-http']
    },
    'config': server_config_schema,
    'enabled': {
        'type': 'boolean',
        'default': True,
    }
}


def server_validator(require_all=True):
    return Validator(server_schema, require_all=require_all)


to_bool = lambda v: v.lower() in ('true', '1')

paging_schema = {
    'page': {
        'type': 'integer',
        'min': 1,
        'default': 1,
        'coerce': int
    },
    'itemsPerPage': {
        'type': 'integer',
        'min': -1,
        'max': 15,
        'default': 5,
        'coerce': int
    }
}


def with_paging(schema):
    schema = dict(paging_schema, **schema)
    return Validator(schema, purge_unknown=True)


def paging_validator():
    return Validator(paging_schema)