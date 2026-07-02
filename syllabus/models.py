from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=30, verbose_name="Название")
    image = models.ImageField(upload_to="images/courses/", verbose_name="Превью", blank=True, null=True)
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        to="users.CustomUser", on_delete=models.CASCADE, related_name="courses", verbose_name="Владелец"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее_обновление")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="images/lessons/", verbose_name="Превью", blank=True, null=True)
    link = models.URLField(verbose_name="Ссылка_на_видео", blank=True, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    owner = models.ForeignKey(
        to="users.CustomUser", on_delete=models.CASCADE, related_name="lessons", verbose_name="Владелец"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее_обновление")

    def __str__(self):
        return f"{self.title} - {self.course}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        to="users.CustomUser", on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Пользователь"
    )
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Курс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата_создания")

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
        unique_together = ("user", "course")
