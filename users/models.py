from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=35, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь")
    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата_оплаты")
    course = models.ForeignKey(to="syllabus.Course", on_delete=models.SET_NULL, null=True, related_name="payments", verbose_name="Оплаченый_курс")
    lesson = models.ForeignKey(to="syllabus.Lesson", on_delete=models.SET_NULL, null=True, related_name="payments", verbose_name="Оплаченый_урок")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма_оплаты")
    payment_method = models.BooleanField(default=True, verbose_name="Способ_оплаты")

    def __str__(self):
        return f"{self.user} - {self.course if self.course else self.lesson} - {self.payment_date}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
