def test_paths(client):
    paths = ['/', '/servers', '/login']
    for path in paths:
        print("Path", path)
        rv = client.get(path)
        assert rv.status_code == 200