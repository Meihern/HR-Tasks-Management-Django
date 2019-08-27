from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from Fiche_Evaluation.permissions import *


class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = 'Dashboard.html'

    def get(self, request, *args, **kwargs):
        if can_add_fiche_objectif(request.user):
            can_add_fiche = True
        else:
            can_add_fiche = False
        return render(request, self.template_name, context={'can_add_fiche': can_add_fiche})


class ConsultationView(TemplateView, LoginRequiredMixin):
    template_name = 'Gestion_Attestations/consultation_attestations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class DemandeMonEquipeView(TemplateView, LoginRequiredMixin):
    template_name = 'equipe.html'

    def get(self, request, *args, **kwargs):
        current_employe = request.user
        equipe = Employe.objects.filter(superieur_hierarchique=current_employe).values('matricule_paie')
        data_equipe = []
        for e in equipe:
            e = Employe.objects.get(matricule_paie=e['matricule_paie'])
            employe = {
                'matricule': e.get_matricule(),
                'nom_prenom': e.get_full_name(),
            }
            data_equipe.append(employe)

        return render(request, self.template_name, context={'equipe': data_equipe})


class DemanderServiceSuperieur(TemplateView, LoginRequiredMixin):
    template_name = 'Dashboard_equipe.html'

    def get(self, request, employe_id, *args, **kwargs):
        current_employe = get_object_or_404(Employe, pk=employe_id)
        if current_employe.get_superieur_hierarchique() != request.user:
            return HttpResponseForbidden()
        return render(request, self.template_name, context={'nom_prenom': current_employe.get_full_name(),
                                                            'matricule': employe_id})


def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response("403.html")
    response.status_code = 500
    return response


def handler403(request, exception, template_name="403.html"):
    response = render_to_response(template_name)
    response.status_code = 403
    return response




