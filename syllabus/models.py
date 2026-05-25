from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=30, verbose_name="Название")
    image = models.ImageField(upload_to="images/courses/", verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="images/lessons/", verbose_name="Превью")
    link = models.URLField(verbose_name="Ссылка_на_видео")
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")

    def __str__(self):
        return f"{self.title} - {self.course}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
