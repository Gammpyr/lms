from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payments', views.PaymentViewSet, basename='payments')

urlpatterns = [
    path('users/update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateAPIView.as_view(), name='user-create'),
] + router.urls
