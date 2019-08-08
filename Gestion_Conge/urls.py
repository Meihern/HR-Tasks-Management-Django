from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^demande_conge$', login_required(views.DemandeCongeView.as_view()), name='demande_conge'),
]