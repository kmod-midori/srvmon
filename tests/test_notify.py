import requests_mock, requests


def test_mail(app, mail):
    from app.db import Server, Record, Contact
    from app.notify import deliver_email

    server = Server(label="TEST_SRV")
    record = Record(online=True)
    contact = Contact(type='email')
    contact.set_config(dict(address="test@example.com"))

    with mail.record_messages() as outbox:
        deliver_email(server, record, contact)
        assert len(outbox) == 1
        assert outbox[0].subject == "TEST_SRV is ONLINE"

        record = Record(online=False, message="Timed out")
        deliver_email(server, record, contact)
        assert len(outbox) == 2
        assert outbox[1].subject == "TEST_SRV is OFFLINE"


def test_webhook(app):
    from app.db import Server, Record, Contact
    from app.notify import deliver_webhook

    server = Server(label="TEST_SRV")
    record = Record(online=True)
    contact = Contact(type='webhook')
    url = "https://oapi.dingtalk.com/robot/send?access_token="
    contact.set_config(dict(url=url, service='ding'))

    with requests_mock.Mocker() as m:
        m.post(url, json={}, status_code=200)
        deliver_webhook(server, record, contact)

        assert m.called
        json = m.last_request.json()
        assert json == {
            'msgtype': 'text',
            'text': {
                'content': 'Server TEST_SRV is currently ONLINE'
            }
        }
