from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from syllabus.models import Course, Lesson, Subscription
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
    is_subscribed = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.INT)
    def get_lesson_count(self, instance):
        return instance.lessons.count()

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_subscribed(self, instance):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=instance).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["owner"]


class SubscriptionSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ["id", "user", "course", "created_at"]
        read_only_fields = ["course", "user"]
