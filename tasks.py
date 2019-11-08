from celery import Celery
from celery.schedules import crontab

from fill_up_db import add_states_to_db
from get_plane_states import get_states


celery_app = Celery('tasks',broker='redis://localhost:6379/0')

@celery_app.task
def fill_up():
    list_states = get_states()
    add_states_to_db(list_states)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/15'), fill_up.s())