from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^remplir_objectifs$', login_required(views.FicheEvaluationView.as_view()), name='remplir_objectifs'),
    url('^consultation_objectifs_personnels$', login_required(views.ConsultationObjectifsView.as_view()), name='consultation_objectifs'),
    path('evaluation/<int:fiche_id>', login_required(views.EvaluationView.as_view()), name='evaluation'),
    url('^evaluation_equipe$', login_required(views.EquipeEvaluationView.as_view()), name='evaluation_equipe'),
    url('^envoyer_commentaire_employe$', login_required(views.set_commentaire_employe), name='envoi_commentaire_employe'),
    url('^envoyer_commentaire_manager$', login_required(views.set_commentaire_manager), name='envoi_commentaire_manager'),
    url('^consultation_objectifs_equipe$', login_required(views.EquipeView.as_view()), name='consultation_objectifs_equipe'),
    path('consultation_objectifs/<int:fiche_id>', login_required(views.ConsultationObjectifsSuperieurView.as_view()), name='consultation_objectif_superieur')
]
