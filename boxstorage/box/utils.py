from django.utils import timezone
from .models import Box


def get_boxes_added_this_week():
    current_week_start = timezone.now().date(
    ) - timezone.timedelta(days=timezone.now().weekday())
    return Box.objects.filter(creation_date__gte=current_week_start)


def get_user_boxes_added_this_week(user):
    current_week_start = timezone.now().date(
    ) - timezone.timedelta(days=timezone.now().weekday())
    return Box.objects.filter(creator=user, creation_date__gte=current_week_start)
