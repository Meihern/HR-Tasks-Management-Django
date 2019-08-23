from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^remplir_objectifs$', login_required(views.FicheEvaluationView.as_view()), name='remplir_objectifs'),
    path('evaluation/<int:fiche_id>', login_required(views.EvaluationView.as_view()), name='evaluation'),
    url('^equipe$', login_required(views.EquipeView.as_view()), name='equipe'),
]
