from .celery import app
from time import sleep
from random import randint


@app.task(queue='high-pri')
def say_hello(msg="Celery"):
    return f"Hello {msg}"


@app.task
def add():
    result = 0
    for i in range(90):
        sleep(5)
        result += randint(1, 99999)
    return result


@app.task
def add2():
    result = 0
    for i in range(90):
        sleep(2)
        result += randint(1, 99999) + 2
    return result


@app.task(queue='low-pri')
def mul():
    result = 1
    for i in range(90):
        sleep(2)
        result *= randint(1, 99999)
    return result


@app.task
def mul2():
    result = 1
    for i in range(90):
        sleep(2)
        result *= randint(1, 99999) * 2
    return result


@app.task
def sqr():
    result = 1
    for i in range(90):
        sleep(2)
        result *= randint(1, 99999) ** 2
    return result


@app.task
def cube():
    result = 1
    for i in range(90):
        sleep(2)
        result *= randint(1, 999) ** 3
    return result
