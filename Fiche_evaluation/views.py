from django.shortcuts import render
from django.views.generic import TemplateView



class FicheEvaluationView(TemplateView):
    template_name = 'Fiche_evaluation/fiche_evaluation.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class EvaluationView(TemplateView):
    template_name = 'Fiche_evaluation/evaluation.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

class EquipeView(TemplateView):
    template_name = 'Fiche_evaluation/equipe.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)





