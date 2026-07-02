from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from syllabus.paginators import CourseLessonPaginator
from syllabus.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from syllabus.models import Course, Lesson, Subscription
from syllabus.tasks import send_update_course_mail
from users.permissions import IsNotModerator, IsOwner


@extend_schema_view(
    list=extend_schema(
        summary="Получить список курсов",
    ),
    update=extend_schema(
        summary="Изменение существующего объекта курса",
    ),
    partial_update=extend_schema(
        summary="Частичное изменение данных о курсе",
    ),
    create=extend_schema(
        summary="Создание нового курса",
    ),
    destroy=extend_schema(
        summary="Удаление существующего курса",
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseLessonPaginator

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
        elif not request.user.groups.filter(name="Moderators").exists() and self.get_queryset().filter(
            owner=self.request.user
        ):
            queryset = self.get_queryset().filter(owner=self.request.user)
        elif not request.user.groups.filter(name="Moderators").exists() and self.get_queryset().filter(
            subscriptions__user=self.request.user
        ):
            queryset = self.get_queryset().filter(subscriptions__user=self.request.user)
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
        instance = serializer.instance
        differ_time = timezone.now() - instance.updated_at
        differ_time_hours = round((differ_time.total_seconds() / 3600), 2)
        request = self.request
        if request.user.groups.filter(name="Moderators").exists():
            serializer.save()
            send_update_course_mail.delay(instance.id, "Course", differ_time_hours)
        elif not request.user.groups.filter(name="Moderators").exists() and self.get_queryset().filter(
            owner=request.user
        ):
            serializer.save(owner=request.user)
            send_update_course_mail.delay(instance.id, "Course", differ_time_hours)
        else:
            raise PermissionDenied("Недостаточно прав для обновления объекта.")


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPaginator

    @extend_schema(summary="Метод для отображения списка уроков")
    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Moderators").exists():
            queryset = self.get_queryset()
        elif not request.user.groups.filter(name="Moderators").exists():
            queryset = self.get_queryset().filter(owner=self.request.user)
        else:
            raise PermissionDenied("Недостаточно прав для отображения объектов.")
        self.queryset = queryset
        return super().list(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    @extend_schema(summary="Метод для создания нового объекта урока")
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Метод для получения отдельного объекта урока")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.groups.filter(name="Moderators").exists():
            serializer = self.get_serializer(instance)
        elif not request.user.groups.filter(name="Moderators").exists() and instance.owner == request.user:
            serializer = self.get_serializer(instance)
        else:
            raise PermissionDenied("Недостаточно прав для отображения объекта.")
        return Response(serializer.data)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Метод устанавливающий порядок редактирования урока: для Пользователя или Модератора")
    def perform_update(self, serializer):
        instance = serializer.instance
        differ_time = timezone.now() - instance.updated_at
        differ_time_hours = round((differ_time.total_seconds() / 3600), 2)
        request = self.request
        if request.user.groups.filter(name="Moderators").exists():
            serializer.save()
            send_update_course_mail.delay(instance.id, "Lesson", differ_time_hours)
        elif not request.user.groups.filter(name="Moderators").exists() and self.get_queryset().filter(
            owner=request.user
        ):
            serializer.save(owner=request.user)
            send_update_course_mail.delay(instance.id, "Lesson", differ_time_hours)
        else:
            raise PermissionDenied("Недостаточно прав для обновления объекта.")


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator, IsOwner]


class SubscriptionView(APIView):

    @extend_schema(summary="Метод для изменения статуса подписки пользователя")
    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})
