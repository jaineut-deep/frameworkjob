from rest_framework.exceptions import PermissionDenied
from syllabus.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from syllabus.models import Course, Lesson
from users.permissions import IsNotModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        elif self.action == "create":
            return [IsAuthenticated(), IsNotModerator()]
        elif self.action == "retrieve":
            return [IsAuthenticated()]
        elif self.action == "update":
            return [IsAuthenticated()]
        elif self.action == "partial_update":
            return [IsAuthenticated()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsNotModerator(), IsOwner()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Moderators").exists():
            queryset = self.get_queryset()
        elif not request.user.groups.filter(name="Moderators").exists():
            queryset = self.get_queryset().filter(owner=self.request.user)
        else:
            raise PermissionDenied("Недостаточно прав для отображения объектов.")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.groups.filter(name="Moderators").exists():
            serializer = self.get_serializer(instance)
        elif not request.user.groups.filter(name="Moderators").exists() and instance.owner == request.user:
            serializer = self.get_serializer(instance)
        else:
            raise PermissionDenied("Недостаточно прав для отображения объекта.")
        return Response(serializer.data)

    def perform_update(self, serializer):
        request = self.request
        if request.user.groups.filter(name="Moderators").exists():
            serializer.save()
        elif (not request.user.groups.filter(name="Moderators").exists() and
            self.get_queryset().filter(owner=request.user)):
            serializer.save(owner=request.user)
        else:
            raise PermissionDenied("Недостаточно прав для обновления объекта.")


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
