from django.conf.urls import url
from django.urls import re_path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^login$', views.AuthenticationView.as_view(redirect_authenticated_user=True), name='login'),
    url('^logout$', views.logout_view, name='logout'),
    url('^reset_password_email$', views.SendPasswordResetEmail.as_view(), name='reset_password_email'),
    re_path('^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            views.ResetPasswordView.as_view(), name='reset_password_confirm'),
    url('^profile$', login_required(views.ProfileView.as_view()), name='profile'),
]
