from app import app
import requests, sys, eventlet, socket
from datetime import datetime, timedelta
from .db import Server, Record, transaction, db
from .notify import notify_state_changed
from blinker import Namespace


def log_start(server):
    app.logger.debug("Start checking [%s](%s)", server.label, server.id)


def log_record(record):
    if record.online:
        app.logger.debug("%d is online", record.server_id)
    else:
        app.logger.debug("%d is offline: %s", record.server_id, record.message)


def log_state_changed(server, record):
    app.logger.info("State of %s changed, online: %s", server.label,
                    str(record.online))


def handle_active_http(server):
    """
    Handler for Active HTTP checking
    """
    config = server.get_config()
    timeout = config['timeout']
    url = config['url']
    valid_status = config['validStatus']

    record = server.new_record()
    try:
        r = requests.get(url, timeout=float(timeout) / 1000)
        if r.status_code in valid_status:
            record.online = True
            record.latency = int(r.elapsed / timedelta(milliseconds=1))
        else:
            record.message = f"Unsuccessful status code: {r.status_code}"
    except requests.exceptions.Timeout as e:
        record.message = "Timed out"
    except requests.exceptions.ConnectionError as e:
        record.message = "Connection error"
        app.logger.debug("Check failed for [%s]: %s", server.label, e)
    except:
        e = sys.exc_info()[0]
        record.message = str(e)
        app.logger.debug("Check failed for [%s]: %s", server.label, e)

    return record


def handle_active_tcp(server):
    """
    Handler for Active TCP checking
    """
    config = server.get_config()
    timeout = config['timeout']
    address = config['address']
    port = config['port']

    record = server.new_record()
    try:
        c = socket.socket()
        ip = socket.gethostbyname(address)
        c.settimeout(int(timeout / 1000))
        start = datetime.now()
        c.connect((ip, port))
        end = datetime.now()
        c.close()
        record.online = True
        record.latency = (end - start) / timedelta(milliseconds=1)
    except Exception as e:
        record.message = str(e)

    return record


def handle_passive_http(server):
    # print(server)
    pass


def handle_server(server):
    """
    Common handler for any server
    """
    config = server.get_config()
    interval = config['interval']

    last_record = server.last_record()
    if last_record and not last_record.expired(interval):
        return

    log_start(server)
    record = handlers[server.mode](server)
    log_record(record)

    with transaction():
        db.session.add(record)

    signal_new_record.send(record=record)

    if last_record and record.online != last_record.online:
        log_state_changed(server, record)
        notify_state_changed(server, record)


def task_check():
    servers = Server.query.filter_by(enabled=True).all()
    threads = []
    for server in servers:
        threads.append(eventlet.spawn(handle_server, server))
    for thread in threads:
        try:
            thread.wait()
        except Exception as e:
            app.logger.error("Error when running task for server: %s", e)


handlers = {
    'active-http': handle_active_http,
    'passive-http': handle_passive_http,
    'active-tcp': handle_active_tcp
}

signals = Namespace()
signal_new_record = signals.signal('new-record')