from rest_framework import serializers

from .models import Course, Lesson
from .validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, obj):
        if obj.course_lessons.all():
            return obj.course_lessons.all().count()
        else:
            return 0

    class Meta:
        model = Course
        fields = '__all__'
        validators = [UrlValidator(field='video_url')]
