from syllabus.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from syllabus.models import Course, Lesson
from users.permissions import IsModerator, IsOwnerOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "update":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "partial_update":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModerator, IsOwnerOrReadOnly]





class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
