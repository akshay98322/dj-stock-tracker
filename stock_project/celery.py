from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_project.settings')

app = Celery('stock_project')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    # 'every-10-sec' : {
    #     'task' : 'core.tasks.update_stocks',
    #     'schedule' : 10,
    #     'args' : (['RELIANCE.NS','ONGC.NS'],)
    # },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')