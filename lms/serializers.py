from rest_framework import serializers

from .models import Course, Lesson, CourseSubscription
from .validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lesson_count(self, obj):
        """ПОдсчитываем количество уроков в курсе"""
        if obj.course_lessons.all():
            return obj.course_lessons.all().count()
        else:
            return 0

    def get_is_subscribed(self, obj):
        """Проверяем подписан ли пользователь на курс"""
        request = self.context.get('request')
        if request:
            return CourseSubscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'
        validators = [UrlValidator(field='video_url')]

class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'
        read_only_fields = ['user', 'created_at']