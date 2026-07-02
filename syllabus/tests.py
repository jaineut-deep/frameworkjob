from unittest import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from syllabus.serializers import LessonSerializer
from users.models import CustomUser
from syllabus.models import Course, Lesson, Subscription


class LessonTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user_test", email="test@example.com", password="qwerty")
        self.user_owner = CustomUser.objects.create_user(
            username="owner_user", email="owner@example.com", password="123qwe"
        )
        self.user_moder = CustomUser.objects.create_user(
            username="moder_user", email="moder@example.com", password="qwe123"
        )
        self.user_moder.groups.add(1)

        self.course = Course.objects.create(title="Test_course", description="Test_description", owner=self.user_owner)
        self.course_alter = Course.objects.create(
            title="Test_course_different", description="Test_description_different", owner=self.user_owner
        )
        self.lessons_one = Lesson.objects.create(
            title="Test_lesson_one", description="Test_practices", course=self.course, owner=self.user_owner
        )
        self.lessons_two = Lesson.objects.create(
            title="Test_lesson_two", description="Test_theory", course=self.course, owner=self.user_owner
        )
        self.lessons_three = Lesson.objects.create(
            title="Test_lesson_three", description="Test_theory_three", course=self.course, owner=self.user_owner
        )

        self.client = APIClient()

    def test_lesson_list_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("syllabus:lesson_list")
        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

        lessons_data = Lesson.objects.filter(owner=self.user_owner)
        serialized_lessons = LessonSerializer(lessons_data, many=True)

        page_size = response.data.get("page_size", 2)
        expected_count = min(len(serialized_lessons.data), page_size)
        self.assertEqual(len(response.data["results"]), expected_count)

    def test_lesson_create_moder(self):
        self.client.force_authenticate(user=self.user_moder)
        url = reverse("syllabus:lesson_create")
        data = {"title": "Test_title", "description": "Test_description"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("syllabus:lesson_create")
        data = {
            "title": "Test_title",
            "description": "Test_description",
            "course": self.course.id,
            "owner": self.user_owner.id,
        }
        response = self.client.post(url, data)
        lesson_data = Lesson.objects.get(title="Test_title", description="Test_description")
        serialized_lesson = LessonSerializer(lesson_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), serialized_lesson.data)

    def test_lesson_retrieve_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("syllabus:lesson_retrieve", args=(self.lessons_one.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lessons_one.title)

    def test_lesson_update_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("syllabus:lesson_update", args=(self.lessons_one.pk,))
        data = {"description": "Test_alter_description", "course": self.course.id, "owner": self.user.id}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("syllabus:lesson_update", args=(self.lessons_one.pk,))
        data = {"description": "Test_alter_description", "course": self.course.id, "owner": self.user_owner.id}
        response = self.client.patch(url, data)
        data_output = response.json()
        self.lessons_one.refresh_from_db()
        serialized_lesson = LessonSerializer(self.lessons_one)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_output.get("description"), serialized_lesson.data.get("description"))

    def test_lesson_update_moder(self):
        self.client.force_authenticate(user=self.user_moder)
        url = reverse("syllabus:lesson_update", args=(self.lessons_one.pk,))
        data = {"description": "Test_alter_description", "course": self.course.id, "owner": self.user_owner.id}
        response = self.client.patch(url, data)
        data_output = response.json()
        self.lessons_one.refresh_from_db()
        serialized_lesson = LessonSerializer(self.lessons_one)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_output.get("description"), serialized_lesson.data.get("description"))

    def test_lesson_destroy_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("syllabus:lesson_delete", args=(self.lessons_two.pk,))
        response = self.client.delete(url)
        data_output = response.json()
        warn_mess = {"detail": "You do not have permission to perform this action."}

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data_output, warn_mess)

    def test_lesson_destroy_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("syllabus:lesson_delete", args=(self.lessons_two.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.filter(owner=self.user_owner).count(), 2)

    def test_lesson_create_wrong(self):
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("syllabus:lesson_create")
        data = {
            "title": "Test_title",
            "description": "Test_description",
            "link": "https://www.rutube.ru",
            "course": self.course.id,
            "owner": self.user_owner.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscription_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("syllabus:subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        mess_out = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mess_out, {"message": "подписка добавлена"})
        self.assertTrue(Subscription.objects.filter(course_id=self.course.id).count() == 1)

        url = reverse("syllabus:subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        mess_out = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mess_out, {"message": "подписка удалена"})
        self.assertTrue(Subscription.objects.filter(course_id=self.course.id).count() == 0)

    def tearDown(self):
        CustomUser.objects.get(username="user_test").delete()
        CustomUser.objects.get(username="owner_user").delete()
        CustomUser.objects.get(username="moder_user").delete()
