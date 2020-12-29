import os, eventlet

from app import app

from .checkers import task_check

def loop_check():
    while True:
        try:
            task_check()
        except Exception as e:
            app.logger.error("Error when running check task: %s", e)
        eventlet.sleep(5)


_is_dev = os.environ.get("FLASK_ENV") == "development"
_is_main = os.environ.get("WERKZEUG_RUN_MAIN") == "true"
_is_testing = app.config['TESTING']

# We don't want multiple instances of the scheduler
if (not _is_testing) and ((not _is_dev) or (_is_dev and _is_main)):
    app.logger.info("Starting scheduler")
    eventlet.spawn_n(loop_check)
