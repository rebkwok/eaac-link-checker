from apscheduler.schedulers.blocking import BlockingScheduler
from eaac import main as checklinks

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def timed_job():
    checklinks()

sched.start()
