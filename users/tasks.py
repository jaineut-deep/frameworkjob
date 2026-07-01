from celery import shared_task
from datetime import datetime, timedelta
from users.models import CustomUser
from zoneinfo import ZoneInfo


@shared_task
def block_user_after_month():
    month_date = datetime.now(ZoneInfo("Europe/Moscow")) - timedelta(days=30)
    users_query = CustomUser.objects.filter(last_login__lt=month_date)
    if users_query:
        users_query.update(is_active=False)
