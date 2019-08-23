from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from Authentification.models import Employe
from Notifications.models import Notification
from .utils import *
from Fiche_Evaluation.models import Objectif, FicheObjectif, SousObjectif
from .forms import FicheObjectifForm, clean_poids


class FicheEvaluationView(FormView):
    form = FicheObjectifForm
    template_name = 'Fiche_Evaluation/fiche_evaluation.html'
    success_url = '/fiche_evaluation/remplir_objectifs'

    def get(self, request, *args, **kwargs):
        # if not  fiche_evalutation_accessible() or request.user.is_consultant:
        if request.user.is_consultant:
            return HttpResponseForbidden()
        return render(request, template_name=self.template_name, context={'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        employe = request.user
        if employe:
            objectifs = request.POST.getlist(form.FIELD_NAME_MAPPING['objectif'])
            poids = request.POST.getlist(form.FIELD_NAME_MAPPING['poids'])
            if form.is_valid(objectifs, poids):
                fiche_objectif = FicheObjectif(employe=employe)
                fiche_objectif.save()
                result = self.form_valid(form)
                for i in range(len(objectifs)):
                    objectif = Objectif(description=objectifs[i], fiche_objectif=fiche_objectif,
                                        poids=poids[i] / 100)
                    objectif.save()
                    sous_objectifs = request.POST.getlist(
                        form.FIELD_NAME_MAPPING['sous_objectif'].replace('_objectif_id', str(i + 1)))
                    if sous_objectifs:
                        for desc_sous_objectif in sous_objectifs:
                            sous_objectif = SousObjectif(description=desc_sous_objectif, objectif=objectif)
                            sous_objectif.save()
                    try:
                        notification = Notification(content_object=fiche_objectif, no_reply=True)
                        notification.set_subject("Nouvelle Fiche d'objectif")
                        notification.set_message(str(fiche_objectif))
                        notification.set_sender(employe)
                        notification.set_receiver()
                        notification.save()
                        messages.success(request, "Votre fiche d'objectifs a été remplie avec succès")
                    except:
                        messages.error(request, "Une erreur est survenue")
                    return result
            else:
                result = self.form_invalid(form)
                messages.error(request, str(form.errors))
                return result
        else:
            return HttpResponseForbidden()


class EquipeView(TemplateView):
    template_name = 'Fiche_Evaluation/equipe.html'

    def get(self, request, *args, **kwargs):
        # if not evaluation_mi_annuelle_accessible() or not evaluation_annuelle_accessible() or request.user.is_consultant:
        #    return HttpResponseForbidden()
        employe = request.user
        equipe = Employe.objects.filter(superieur_hierarchique=employe)
        fiche_objectifs = FicheObjectif.objects.filter(employe__in=equipe)
        fiche_objectifs = fiche_objectifs.all().values('id')
        data = []
        for fiche in fiche_objectifs:
            fiche = FicheObjectif.objects.safe_get(id=fiche['id'])
            if fiche.is_current:
                fiche_objectif = {
                    'id': fiche.id,
                    'employe': fiche.get_employe().get_full_name(),
                }
                data.append(fiche_objectif)
        return render(request, template_name=self.template_name, context={'fiche_objectifs': data})


class EvaluationView(TemplateView):
    template_name = 'Fiche_Evaluation/evaluation'

    def get_template_mi_annuelle(self):
        self.template_name += '_mi_annuelle.html'

    def get_template_annuelle(self):
        self.template_name += '_annuelle.html'

    def get(self, request, fiche_id, *args, **kwargs):
        fiche_objectif = FicheObjectif.objects.get(id=fiche_id)

        if request.user.is_consultant:
            return HttpResponseForbidden()

        if not request.user.is_superieur_to(fiche_objectif.get_employe()):
            return HttpResponseForbidden()

        if evaluation_annuelle_accessible():        # Reminder to change the month condition to 6
            self.get_template_annuelle()
        elif evaluation_mi_annuelle_accessible():   # Reminder to change the month condition to 12
            self.get_template_mi_annuelle()
        else:
            return HttpResponseForbidden()

        objectifs = fiche_objectif.get_objectifs()
        data_objectifs = []
        for data in objectifs:
            objectif = Objectif.objects.get(id=data['id'])
            sous_objectifs = objectif.get_sous_objectifs()
            data_sous_objectifs = []
            for data2 in sous_objectifs:
                sous_objectif = SousObjectif.objects.get(id=data2['id'])
                sous_objectif = {
                    'id_sous_objectif': sous_objectif.id,
                    'description': sous_objectif.get_description()
                }
                data_sous_objectifs.append(sous_objectif)
            objectif = {
                'id_objectif': objectif.id,
                'description': objectif.get_description(),
                'sous_objectifs': data_sous_objectifs,
                'poids': objectif.get_poids()
            }
            data_objectifs.append(objectif)

        return render(request, template_name=self.template_name, context={'objectifs': data_objectifs})
