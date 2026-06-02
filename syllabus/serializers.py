from rest_framework import serializers
from syllabus.models import Course, Lesson
from syllabus.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ["owner"]
        validators = [LinkValidator(field="link")]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["owner"]
