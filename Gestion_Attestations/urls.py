from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url('^demande_doc$', login_required(views.envoyer_demande_doc), name='demande_doc'),
    url('^demande_attestations$', login_required(views.DemandeAttestationView.as_view()), name='demande_attestations'),
    url('^accept_demande_doc$',login_required(views.accept_demande_doc), name='accept_demande_doc'),
    path('consultation_demandes_docs/<str:type_doc>',
         login_required(views.ConsultationDemandesDoc.as_view()), name='consultation_demandes_docs'),
    url('^historique_demandes$', login_required(views.HistoriqueDemandesAttestationsView.as_view()), name='historique_demandes_attestations'),
]
