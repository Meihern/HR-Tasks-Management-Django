from django.conf.urls import url
from . import views
urlpatterns = [
    url('^get_notifications$', views.get_notifications, name='get_notifications'),
    url('^get_notification_detail$', views.get_notification_detail, name='get_notification_detail'),
    url('^get_notifications_count$', views.get_notifications_count, name='get_notifications_count'),
]
