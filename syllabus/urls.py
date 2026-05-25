from django.urls import path
from rest_framework.routers import DefaultRouter
from syllabus.apps import SyllabusConfig
from syllabus.views import (CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView,
                            LessonUpdateAPIView, LessonDestroyAPIView)

app_name = SyllabusConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
] + router.urls
