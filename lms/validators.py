import re

from rest_framework.exceptions import ValidationError


class UrlValidator:
    """Валидатор для проверки ссылок (разрешен только ютуб)"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = re.compile(r"(youtube\.com|youtu\.be)")
        field_value = value.get(self.field)

        if field_value and not bool(pattern.search(field_value)):
            raise ValidationError("Запрещены ссылки на сторонние ресурсы, кроме YouTube")
