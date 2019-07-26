from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^generate_pdf$',login_required(views.GeneratePDF.as_view()), name='generate_pdf'),
]