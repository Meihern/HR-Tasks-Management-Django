from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import FicheObjectifForm


class FicheEvaluationView(FormView):
    form = FicheObjectifForm
    template_name = 'Fiche_Evaluation/fiche_evaluation.html'
    success_url = '.'

    def get(self, request, *args, **kwargs):
        if request.user.is_consultant:
            return HttpResponseForbidden()
        return render(request, template_name=self.template_name, context={'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        employe = request.user
        pass


class EvaluationView(TemplateView):
    template_name = 'Fiche_Evaluation/evaluation.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

class EquipeView(TemplateView):
    template_name = 'Fiche_Evaluation/equipe.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)





