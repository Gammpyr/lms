import re

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
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        """Проверяем подписан ли пользователь на курс"""
        request = self.context.get('request')
        if request:
            return CourseSubscription.objects.filter(user=request.user, course=obj).exists()
        return False

    def validate(self, attrs):
        video_url = attrs.get('video_url')
        if video_url and not re.search(r'(youtube\.com|youtu\.be)', video_url):
            raise serializers.ValidationError({'video_url': 'Разрешены только ссылки на YouTube'})
        return attrs

    class Meta:
        model = Course
        fields = '__all__'
        validators = [UrlValidator(field='video_url')]
        read_only_fields = ['notification_task_id', 'owner', 'updated_at']

class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'
        read_only_fields = ['user', 'created_at']