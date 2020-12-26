from app import app
import requests, sys
from datetime import datetime, timedelta
from .db import Server, Record, transaction, db

def log_start(server):
    app.logger.debug("Start checking [%s](%s)", server.label, server.id)


def log_record(record):
    if record.online:
        app.logger.debug("%d is online", record.server_id)
    else:
        app.logger.debug("%d is offline: %s", record.server_id, record.message)


def handle_active_http(server):
    """
    Handler for Active HTTP checking
    """
    config = server.get_config()
    timeout = config['timeout']
    url = config['url']
    valid_status = config['validStatus']

    log_start(server)

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
        record.message = str(e)
    except:
        record.message = str(sys.exc_info()[0])

    log_record(record)

    with transaction():
        db.session.add(record)


def handle_active_tcp(server):
    pass


def handle_passive_http(server):
    # print(server)
    pass

handlers = {
    'active-http': handle_active_http,
    'passive-http': handle_passive_http,
    'active-tcp': handle_active_tcp
}