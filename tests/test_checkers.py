import requests_mock, socket, requests


def test_active_http(app):
    from app.checkers import handle_active_http
    from app.db import Server

    url = "https://www.baidu.com"
    server = Server(id=1,
                    label="Test Server",
                    mode="active-http",
                    enabled=True)
    server.set_config(
        dict(url=url, timeout=3000, interval=300, validStatus=[200, 204]))

    with requests_mock.Mocker() as m:
        # Success
        m.get(url, text='resp', status_code=200)
        record = handle_active_http(server)
        assert record.online

        m.get(url, text='resp', status_code=204)
        record = handle_active_http(server)
        assert record.online

        # Error
        m.get(url, text='resp', status_code=500)
        record = handle_active_http(server)
        assert not record.online
        assert record.message == 'Unsuccessful status code: 500'

        m.get(url, exc=requests.exceptions.ConnectTimeout)
        record = handle_active_http(server)
        assert not record.online
        assert record.message == 'Timed out'


def test_active_tcp(app):
    from app.checkers import handle_active_tcp
    from app.db import Server

    # Spawn a real TCP server on a random port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    s.listen(5)
    port = s.getsockname()[1]

    server = Server(id=1, label="Test Server", mode="active-tcp", enabled=True)
    server.set_config(
        dict(timeout=3000, interval=300, address="127.0.0.1", port=port))
        
    # Success
    record = handle_active_tcp(server)
    assert record.online
    s.close()

    # Error
    record = handle_active_tcp(server)
    assert not record.online
