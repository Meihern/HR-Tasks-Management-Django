from django.shortcuts import render
from django.views.generic import TemplateView


class FicheEvaluationView(TemplateView):
    template_name = 'Fiche_Evaluation/fiche_evaluation.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class EvaluationView(TemplateView):
    template_name = 'Fiche_Evaluation/evaluation.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

class EquipeView(TemplateView):
    template_name = 'Fiche_Evaluation/equipe.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)





