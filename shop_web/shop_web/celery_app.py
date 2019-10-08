from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.utils.log import get_task_logger

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_web.settings')

# todo 改為用此方法
# app = Celery('shop_web')

# 指定消息中間件用 redis，URL 為 redis://127.0.0.1:6379
broker = 'redis://127.0.0.1:6379'

# 指定存儲用 redis，URL為 redis://127.0.0.1:6379/0
backend = 'redis://127.0.0.1:6379/0'

# 創建了一個 Celery 實例 app，名稱為 my_task
app = Celery('shop_web', broker=broker, backend=backend)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


if __name__ == '__main__':
    argv = [
        'worker',
        '-B',
        '--loglevel=info',
    ]
    app.worker_main(argv)
