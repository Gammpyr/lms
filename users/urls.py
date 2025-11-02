from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('users/update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateAPIView.as_view(), name='user-create'),
]
