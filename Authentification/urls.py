from django.conf.urls import url
from . import views


urlpatterns = [
    url('^login$', views.AuthenticationView.as_view(redirect_authenticated_user=True), name='login'),
    url('^logout$', views.logout_view, name='logout'),
    url('^reset_password$', views.ResetPasswordView.as_view(), name='reset_password')
]