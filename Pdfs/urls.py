from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('generate_pdf/<int:doc_id>', login_required(views.GeneratePDF.as_view()), name='generate_pdf'),
]