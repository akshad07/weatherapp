from celery import shared_task

@shared_task(time_limit=43200, soft_time_limit=43200)
def weather_celery():
    print("Celery Called")
    pass