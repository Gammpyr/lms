from django.urls import path
from rest_framework.routers import DefaultRouter

from lms import views
from lms.apps import LmsConfig

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", views.CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/create/", views.LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/", views.LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson-get"),
    path(
        "lessons/update/<int:pk>/",
        views.LessonUpdateAPIView.as_view(),
        name="lesson-update",
    ),
    path(
        "lessons/delete/<int:pk>/",
        views.LessonDestroyAPIView.as_view(),
        name="lesson-delete",
    ),
    path("subscription/", views.CourseSubscriptionAPIView.as_view(), name="subscription"),
] + router.urls
