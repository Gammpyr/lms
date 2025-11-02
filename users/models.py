from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(max_length=46, blank=True, null=True, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} ({self.email})'

    @property
    def display_name(self):
        return f'{self.first_name} {self.last_name}' or self.username