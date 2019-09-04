from celery import Celery

app = Celery(__name__,
             broker='redis://localhost:6379/0')

app.autodiscover_tasks(['celery_demo.tasks'])

app.conf.task_routes = {
    'celery_demo.tasks.add': {'queue': 'low-pri'},
    'celery_demo.tasks.add2': {'queue': 'low-pri'},
    # 'celery_demo.tasks.mul': {'queue': 'high-pri'},
    'celery_demo.tasks.mul2': {'queue': 'high-pri'},
}

app.conf.beat_schedule = {
    'say-hello-5-secs': {
        'task': 'celery_demo.tasks.say_hello',
        'schedule': 5.0,
        'args': ('Django',)
    }
}

if __name__ == '__main__':
    app.start()


