def test_empty_contacts(client_l):
    rv = client_l.get('/api/contacts')
    assert len(rv.json['payload']['contacts']) == 0


def test_add_contact(client_l):
    rv = client_l.put('/api/contacts', json=dict())
    assert rv.status_code == 400

    rv = client_l.put('/api/contacts',
                      json=dict(type='email',
                                enabled=True,
                                config=dict(address="test@example.com")))
    assert rv.status_code == 200

    rv = client_l.put('/api/contacts',
                      json=dict(type='webhook',
                                enabled=True,
                                config=dict(url='https://www.example.com',
                                            service='ding')))
    assert rv.status_code == 200


def test_enable_disable_contact(client_l):
    rv = client_l.post('/api/contacts/1', json=dict(enabled=False))
    assert rv.status_code == 200

    rv = client_l.post('/api/contacts/1', json=dict(enabled=True))
    assert rv.status_code == 200

def test_delete_contact(client_l):
    rv = client_l.delete('/api/contacts/1')
    assert rv.status_code == 200
    rv = client_l.delete('/api/contacts/2')
    assert rv.status_code == 200
    test_empty_contacts(client_l)