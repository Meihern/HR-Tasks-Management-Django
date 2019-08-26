from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('generate_pdf_attestation/<int:doc_id>', login_required(views.GeneratePDFAttestations.as_view()), name='generate_pdf'),
    path('generate_pdf_fiche_objectif/<int:fiche_id>', login_required(views.GeneratePDFFichesObjectifs.as_view()), name='generate_pdf_fiche_objectif'),
    path('generate_pdf_demande_conge/<int:demande_conge_id>', login_required(views.GeneratePDFDemandeConge.as_view()), name='generate_pdf_demande_conge'),
]