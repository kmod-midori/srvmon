def test_empty_servers(client_l):
    """Start with a blank DB"""
    rv = client_l.get('/api/servers')
    assert len(rv.json['payload']['items']) == 0


def add_server(client_l, server_data=None):
    if server_data is None:
        server_data = dict(label="Server 1",
                           mode="active-http",
                           config=dict(timeout=1000,
                                       interval=300,
                                       url="http://www.baidu.com",
                                       validStatus=[200, 302]))
    return client_l.put('/api/servers', json=server_data)

def get_server(client_l, srv_id):
    return client_l.get(f'/api/servers/{srv_id}')

def test_add_server(client_l):
    """Add server"""
    # All OK
    rv = add_server(client_l)
    assert rv.json['payload']['id'] > 0
    # Missing params
    rv = add_server(
        client_l,
        dict(label="Server 1",
             mode="active-http",
             config=dict(timeout=1000,
                         interval=300,
                         url="http://www.baidu.com")))
    assert rv.status_code == 400

def test_get_server(client_l):
    rv = get_server(client_l, 1)
    assert rv.status_code == 200
    assert rv.json['payload']['id'] == 1

def test_watch_unwatch_server(client_l):
    rv = client_l.put("/api/servers/1/watch")
    assert rv.status_code == 200

    rv = get_server(client_l, 1)
    assert rv.json['payload']['watching'] == True

    rv = client_l.delete("/api/servers/1/watch")
    assert rv.status_code == 200

    rv = get_server(client_l, 1)
    assert rv.json['payload']['watching'] == False

def test_del_server(client_l):
    rv = client_l.delete("/api/servers/1")
    assert rv.json['payload']['id'] == 1
    rv = get_server(client_l, 1)
    assert rv.status_code == 404
