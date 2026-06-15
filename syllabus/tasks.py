from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from syllabus.models import Course, Lesson


@shared_task
def send_update_course_mail(pk, model, hours):
    course = None
    if model == "Course" and hours > 4:
        course = Course.objects.filter(pk=pk).first()

    elif model == "Lesson" and hours > 4:
        course = Lesson.objects.filter(pk=pk).first().course

    if course is not None:
        subscription_query = course.subscriptions
        users_emails = subscription_query.values_list("user__email", flat=True)
        send_mail(
            subject="Новости с образовательной платформы",
            message=f"Курс {course}, на который вы подписаны, обновился",
            from_email=EMAIL_HOST_USER,
            recipient_list=users_emails
        )
