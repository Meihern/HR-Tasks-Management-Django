from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from Fiche_Evaluation.permissions import *


class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = 'Dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ConsultationView(TemplateView, LoginRequiredMixin):
    template_name = 'Gestion_Attestations/consultation_attestations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ErrorView(TemplateView, LoginRequiredMixin):
    template_name = '404.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ErrorTView(TemplateView, LoginRequiredMixin):
    template_name = '403.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class EquipeView(TemplateView, LoginRequiredMixin):
    template_name = 'equipe.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class DashboardEquipeView(TemplateView, LoginRequiredMixin):
    template_name = 'Dashboard_equipe.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)