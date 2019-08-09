from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(TemplateView,LoginRequiredMixin):
    template_name = 'Dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ConsultationView(TemplateView, LoginRequiredMixin):
    template_name = 'Gestion_Attestations/consultation_attestations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)