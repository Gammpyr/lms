from rest_framework import generics

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class UserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
