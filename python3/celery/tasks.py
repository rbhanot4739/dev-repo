from celery import Celery

app = Celery('tasks',
        broker='redis://:GKCfQWetSvAXtuBegdY8AMB72sAiyZx2f5Y2LfZwRsgEIvu74avAJQ3lp9LKaUgJys-GsrQuMy-wmDkY@localhost:6347/0')
@app.task
def add(x, y):
    return x + y
