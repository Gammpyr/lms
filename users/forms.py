from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        label="Номер телефона",
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autofocus": "true",
            }
        ),
    )
    username = forms.CharField(
        label="Логин",
        max_length=50,
        help_text="Обязательное поле.",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    first_name = forms.CharField(
        label="Имя",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    country = forms.CharField(
        label="Страна",
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        label="Почта",
        help_text="Обязательное поле.",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "autocomplete": "username",
            }
        ),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтверждение пароля"}
        ),
    )
    avatar = forms.ImageField(
        label="Аватар",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "country",
            "phone_number",
            "password1",
            "password2",
            "avatar",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять только из цифр")
        return phone_number

    def clean_country(self):
        country = self.cleaned_data.get("country")
        if country and not country.isalpha():
            raise forms.ValidationError("Страна должна состоять только из букв")
        return country


#
# class CustomAuthenticationForm(AuthenticationForm):
#     error_messages = {
#         'invalid_login': (
#             'Пожалуйста, введите правильную почту и пароль. Обратите внимание, '
#             'что оба поля чувствительны к регистру.'
#         ),
#         'inactive': "Этот аккаунт неактивен.",
#     }
#
#     username = forms.EmailField(
#         label='Почта',
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите вашу почту',
#             'autofocus': True,
#         })
#     )
#     password = forms.CharField(
#         label='Пароль',
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите пароль',
#         })
#     )
