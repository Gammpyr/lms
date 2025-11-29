from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Превью')
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, blank=True, null=True,
                              related_name='courses', verbose_name='Владелец')
    notification_task_id = models.CharField(max_length=255, null=True, blank=True,  verbose_name='ID celery-задачи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['id']


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Превью')
    description = models.TextField(blank=True, verbose_name='Описание')
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, blank=True, null=True,
                              related_name='lessons', verbose_name='Владелец')

    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['id']


class CourseSubscription(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']

    def __str__(self):
        return f'{self.user} - {self.course}'
