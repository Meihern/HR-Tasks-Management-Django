from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url('^demande_doc$', login_required(views.envoyer_demande_doc), name='demande_doc'),
    path('demande_doc_employe/<str:matricule_employe>', login_required(views.envoyer_demande_doc_superieur), name='demande_doc_superieur'),
    url('^demande_attestations$', login_required(views.DemandeAttestationView.as_view()), name='demande_attestations'),
    path('equipe_demande_attestation/<str:employe_id>', login_required(views.AttestationEquipeView.as_view()), name='equipe_demande_attestation'),
    url('^accept_demande_doc$',login_required(views.accept_demande_doc), name='accept_demande_doc'),
    path('consultation_demandes_docs/<str:type_doc>',
         login_required(views.ConsultationDemandesDoc.as_view()), name='consultation_demandes_docs'),
    url('^historique_demandes$', login_required(views.HistoriqueDemandesAttestationsView.as_view()), name='historique_demandes_attestations'),
]
