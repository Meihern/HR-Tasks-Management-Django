from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import TemplateView, FormView

from Fiche_Evaluation.models import Objectif, FicheObjectif
from .forms import FicheObjectifForm, clean_poids


class FicheEvaluationView(FormView):
    form = FicheObjectifForm
    template_name = 'Fiche_Evaluation/fiche_evaluation.html'
    success_url = '/fiche_evaluation/remplir_objectifs'

    def get(self, request, *args, **kwargs):
        #if now().date().month != 1 or request.user.is_consultant:
        if request.user.is_consultant:
            return HttpResponseForbidden()
        return render(request, template_name=self.template_name, context={'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        employe = request.user
        if employe:
            objectifs = request.POST.getlist(form.FIELD_NAME_MAPPING['objectif'])
            poids = request.POST.getlist(form.FIELD_NAME_MAPPING['poids'])
            poids = clean_poids(poids)
            if form.is_valid(objectifs, poids):
                fiche_objectif = FicheObjectif(employe=employe)
                fiche_objectif.save()
                result = self.form_valid(form)
                for i in range(len(objectifs)):
                    objectif = Objectif(description=objectifs[i], fiche_objectif=fiche_objectif, poids=poids[i] / 100)
                    objectif.save()
                messages.success(request, "Votre fiche d'objectifs a été remplie avec succès")
                return result
            else:
                result = self.form_invalid(form)
                messages.error(request, str(form.errors))
                return result
        else:
            return HttpResponseForbidden()


class EvaluationView(TemplateView):
    template_name = 'Fiche_Evaluation/evaluation.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class EquipeView(TemplateView):
    template_name = 'Fiche_Evaluation/equipe.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)
