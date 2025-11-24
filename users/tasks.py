from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def check_user_last_activity():
    """Проверяет пользователей по дате последнего входа и блокирует неактивных"""

    current_date = timezone.now()
    month_ago = current_date - timedelta(days=30)

    users = CustomUser.objects.filter(
        is_active=True,
        last_login__lt=month_ago
    ) | CustomUser.objects.filter(
        is_active=True,
        last_login__isnull=True
    )

    users_count = users.count()
    users.update(is_active=False)


    return {
        'status': 'success',
        'users_blocked': users_count,
    }
