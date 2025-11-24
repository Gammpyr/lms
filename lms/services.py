import json
from datetime import datetime, timedelta

from celery.result import AsyncResult
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from lms.tasks import cancel_delayed_task


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )
    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name='Importing contacts',  # simply describes this periodic task.
        task='config.tasks.import_contacts',  # name of task.
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )


def check_task_creation_time(task_id, updated_at):
    """Проверка времени создания задачи и отмена её, если время не превышает 4 часа."""
    try:
        task = AsyncResult(task_id)

        if task and not task.ready():
            current_time = timezone.now()

            if current_time - updated_at < timedelta(hours=4):
                cancel_delayed_task(task_id)
                print(f'Задача {task_id}({task.name}) отменена')
    except Exception as e:
        print(f'Ошибка во время проверки времени создания задачи: {e}')