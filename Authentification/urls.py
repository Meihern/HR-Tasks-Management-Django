from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^login$', views.AuthenticationView.as_view(redirect_authenticated_user=True), name='login'),
    url('^logout$', views.logout_view, name='logout'),
    url('^reset_password$', views.ResetPasswordView.as_view(), name='reset_password'),
    url('^profile$', login_required(views.ProfileView.as_view()), name='profile'),
    url('^historique_demandes$', login_required(views.HistoriqueDemandesView.as_view()), name='historique_demandes'),
]
