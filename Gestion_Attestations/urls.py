from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url('^demande_doc$', login_required(views.envoyer_demande_doc), name='demande_doc'),
]
