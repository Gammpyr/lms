from celery import shared_task
from celery.result import AsyncResult
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config.settings import DEFAULT_FROM_EMAIL
from lms.models import Course, CourseSubscription


@shared_task
def send_email_after_delay(course_id):
    """Отправляет письмо после задержки"""
    try:
        course = get_object_or_404(Course, id=course_id)
        subscribers = CourseSubscription.objects.filter(course=course).select_related(
            'user')  # получаем всех подписчиков курса
        subscribers_email = [subscriber.user.email for subscriber in
                             subscribers]  # получаем email всех подписчиков курса

        if not subscribers_email:
            return "Нет подписчиков на курсе"

        send_mail(
            subject=f'Курс {course.name} был обновлен!',
            message='Ознакомьтесь с изменениями на странице курса',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=subscribers_email,
            fail_silently=False,
        )

        course.notification_task_id = None
        course.save()

        return f"Письма подписчикам курса {course.name} успешно отправлены!"
    except Exception as e:
        print(f"Ошибка при отправке: {e}")
        return f"Ошибка: {str(e)}"


def cancel_delayed_task(task_id):
    """Отменяет отложенную задачу по ее ID"""
    try:
        result = AsyncResult(task_id)
        result.revoke(terminate=True)
        print(f"Задача {task_id} отменена")
    except Exception as e:
        print(f"Ошибка при отмене задачи: {e}")


