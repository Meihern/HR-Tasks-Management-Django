from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url('^demande_travail$', login_required(views.envoyer_demande_travail), name='demande_travail'),
    url('^demande_salaire$', login_required(views.envoyer_demande_travail), name='demande_salaire'),
    url('^demande_domiciliation', login_required(views.envoyer_demande_travail), name='demande_domiciliation'),
]
