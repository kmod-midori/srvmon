import atexit

from apscheduler.schedulers.background import BackgroundScheduler

cron = BackgroundScheduler()
cron.start()

# Shutdown the cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))
