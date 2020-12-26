import atexit, os
from apscheduler.schedulers.background import BackgroundScheduler

from .db import Server
from app import app

from .checkers import handlers


def task_loop():
    servers = Server.query.filter_by(enabled=True).all()
    for server in servers:
        if server.should_check():
            handlers[server.mode](server)


_is_dev = os.environ.get("FLASK_ENV") == "development"
_is_main = os.environ.get("WERKZEUG_RUN_MAIN") == "true"

if (not _is_dev) or (_is_dev and _is_main):
    app.logger.info("Starting scheduler")

    cron = BackgroundScheduler()
    cron.start()

    # Shutdown the cron thread if the web process is stopped
    atexit.register(lambda: cron.shutdown(wait=False))

    cron.add_job(task_loop, 'interval', seconds=5)