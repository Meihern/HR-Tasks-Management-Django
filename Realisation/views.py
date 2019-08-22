from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from Fiche_Evaluation.utils import fiche_evalutation_accessible


class DashboardView(TemplateView,LoginRequiredMixin):
    template_name = 'Dashboard.html'

    def get(self, request, *args, **kwargs):
        is_fiche_accessible = fiche_evalutation_accessible()
        return render(request, self.template_name, context={'is_fiche_accessible': is_fiche_accessible})


class ConsultationView(TemplateView, LoginRequiredMixin):
    template_name = 'Gestion_Attestations/consultation_attestations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)