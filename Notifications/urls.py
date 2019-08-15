from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
urlpatterns = [
    url('^get_notifications$', login_required(views.get_notifications), name='get_notifications'),
    url('^get_notification_detail$', login_required(views.get_notification_detail), name='get_notification_detail'),
    url('^get_notifications_count$', login_required(views.get_notifications_count), name='get_notifications_count'),
]
