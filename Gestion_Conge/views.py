from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class GestionCongeView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
