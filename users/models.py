from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(max_length=46, blank=True, null=True, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} ({self.email})"

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}" or self.username


class Payment(models.Model):
    PAYMENT_METHODS = [("cash", "Наличные"), ("transfer", "Перевод")]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")
    paid_course = models.ForeignKey(
        Course,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="paid_users",
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="paid_users",
        verbose_name="Оплаченный урок",
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        default="transfer",
        verbose_name="Метод оплаты",
    )
    price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID цены")
    product_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID продукта")
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID сессии")
    payment_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на оплату")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
