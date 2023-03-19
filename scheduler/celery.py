from celery import Celery


app = Celery('scheduler',)

app.config_from_object("scheduler.celeryconfig")

app.control.purge()

app.conf.beat_schedule={
    'run_every_30_seconds': {
        'task': 'scheduler.tasks.load_transactions',
        'schedule': 30.0,
        'args': ()
    }
}



if __name__ == '__main__':
    app.start()