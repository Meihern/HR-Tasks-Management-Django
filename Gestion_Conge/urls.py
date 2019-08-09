from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^demande_conge$', login_required(views.DemandeCongeView.as_view()), name='demande_conge'),
    url('^accept_demande_conge$', login_required(views.accept_demande_conge), name='accept_demande_conge'),
    url('^refuser_demande_conge$', login_required(views.refuser_demande_conge), name='refuser_demande_conge'),
    url('consultation_demande_conge', login_required(views.ConsultationDemandeConges.as_view()), name='consultation_demande_conge')
]
