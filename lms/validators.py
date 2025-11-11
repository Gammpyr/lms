import re

from rest_framework.exceptions import ValidationError


class UrlValidator:
    """Валидатор для проверки ссылок (разрешен только ютуб)"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = re.compile(r'youtube\.com')
        print(value)
        validate_url = dict(value).get(self.field)
        if validate_url is None or validate_url == '':
            return
        if not bool(pattern.search(validate_url)):
            raise ValidationError('Запрещены ссылки на сторонние ресурсы')

