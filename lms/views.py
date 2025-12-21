from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, CourseSubscription
from lms.paginators import LessonPagination, CoursePagination
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer
from lms.services import check_task_creation_time
from lms.tasks import send_email_after_delay, cancel_delayed_task


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', ]:
            permission_classes = [IsModerator | IsOwner]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action in ['destroy']:
            permission_classes = [IsOwner]
        else:
            return super().get_permissions()
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_update(self, serializer):
        # добавить ласт апдейт к моделям урока и курса
        # спустя 4 часа после последнего обновления
        # разослать письма всем подписчикам курса

        instance = self.get_object()
        old_task_id =  instance.notification_task_id
        old_updated_at = instance.updated_at

        instance = serializer.save()

        if old_task_id:
            check_task_creation_time(old_task_id, old_updated_at)

        task = send_email_after_delay.apply_async(
            args=[instance.id],
            countdown=4 * 60 * 60
        )
        instance.notification_task_id = task.id
        instance.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class CourseSubscriptionAPIView(APIView):
    """Управление подпиской на курс"""
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = CourseSubscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            CourseSubscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
