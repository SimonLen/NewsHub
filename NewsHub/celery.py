import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsHub.settings')

app = Celery('NewsHub')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weekly_digest_emails': {
        'task': 'news.tasks.new_post_in_category_notifier',
        'schedule': crontab(minute=0, hour=8, day_of_week='monday'),
    },
}
