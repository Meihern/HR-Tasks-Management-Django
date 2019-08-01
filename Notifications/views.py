from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification
# Create your views here.


def get_notifications(request):

    employe = request.user
    notifications = Notification.objects.filter(receiver=employe, seen=False)
    notifications = notifications.all().values('id','time_sent','subject','message').order_by('-time_sent')
    data = {}
    try:
        data['notifications'] = list(notifications)
    except:
        data['error'] = 'Aucune notification'

    return JsonResponse(data)


def get_notification_detail(request):
    notification = Notification.objects.get(id=request.GET.get('notif_id'))
    notification.update_seen_status()
    notification_message = notification.get_message()
    notification_subject = str(notification)
    data = {'message': notification_message, 'subject': notification_subject}
    return JsonResponse(data)

def get_notifications_count(request):
    employe = request.user
    notifications_count = Notification.objects.filter(receiver=employe, seen=False).count()
    return JsonResponse({'notifications_count': notifications_count})

