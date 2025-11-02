from rest_framework import serializers

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)

    def get_lesson_count(self, obj):
        if obj.lessons.all():
            return obj.lessons.all().count()
        else:
            return 0

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
