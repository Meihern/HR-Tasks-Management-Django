from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.views.generic import TemplateView, FormView

from Authentification.models import Employe
from Notifications.models import Notification
from Realisation.settings import LOGIN_REDIRECT_URL, DEFAULT_FROM_EMAIL
from .utils import *
from Fiche_Evaluation.models import FicheObjectif, Objectif, SousObjectif
from .forms import FicheObjectifForm, EvaluationMiAnnuelleForm, EvaluationAnnuelleForm
from .permissions import can_add_fiche_objectif, get_accessibilite_evaluation_mi_annuelle, get_accessibilite_evaluation_annuelle, get_accessibilite_remplir


class FicheEvaluationView(FormView):
    form = FicheObjectifForm
    template_name = 'Fiche_Evaluation/fiche_evaluation.html'
    success_url = LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        # if not  fiche_evalutation_accessible() or request.user.is_consultant:
        # if request.user.is_consultant:
        #    return HttpResponseForbidden()
        if not get_accessibilite_remplir():
            return HttpResponseForbidden()
        if not can_add_fiche_objectif(request.user):
            return HttpResponseForbidden()
        return render(request, template_name=self.template_name, context={'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        employe = request.user
        if can_add_fiche_objectif(employe):
            objectifs = request.POST.getlist(form.FIELD_NAME_MAPPING['objectif'])
            poids = request.POST.getlist(form.FIELD_NAME_MAPPING['poids'])
            if form.is_valid(objectifs, poids):
                fiche_objectif = FicheObjectif(employe=employe)
                fiche_objectif.save()
                try:
                    notification = Notification(content_object=fiche_objectif, no_reply=True)
                    notification.set_subject("Nouvelle Fiche d'objectif")
                    notification.set_message(str(fiche_objectif))
                    notification.set_sender(employe)
                    notification.set_receiver()
                    notification.save()
                    messages.success(request, "Votre fiche d'objectifs a été remplie avec succès")
                    send_mail(notification.get_subject(), notification.get_message(), DEFAULT_FROM_EMAIL,
                              [notification.get_receiver().get_email()], fail_silently=False)
                except ValueError:
                    result = self.form_invalid(form)
                    messages.error(request, "Une erreur est survenue")
                    fiche_objectif.delete()
                    return result
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
                return result
            else:
                result = self.form_invalid(form)
                messages.error(request, str(form.errors))
                return result
        else:
            return HttpResponseForbidden()


def load_equipe_current_fiches(employe: Employe):
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
                'fonction': fiche.get_employe().get_fonction()
            }
            data.append(fiche_objectif)
    return data


class EquipeEvaluationView(TemplateView):
    template_name = 'Fiche_Evaluation/equipe_evaluation.html'

    def get(self, request, *args, **kwargs):
        # if not evaluation_mi_annuelle_accessible() or not evaluation_annuelle_accessible() or request.user.is_consultant:
        #    return HttpResponseForbidden()
        if not get_accessibilite_evaluation_mi_annuelle() and not get_accessibilite_evaluation_annuelle():
            return HttpResponseForbidden()

        employe = request.user
        data = load_equipe_current_fiches(employe)
        return render(request, template_name=self.template_name, context={'fiche_objectifs': data})


class EquipeView(TemplateView):
    template_name = 'Fiche_evaluation/consultation_equipe_objectifs.html'

    def get(self, request, *args, **kwargs):
        data = load_equipe_current_fiches(request.user)
        return render(request, template_name=self.template_name, context={'fiche_objectifs': data})


def load_fiche_data(fiche_objectif: FicheObjectif):
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
            'poids': get_percentage_value(objectif.get_poids()),
            'evaluation_mi_annuelle': objectif.get_evaluation_mi_annuelle() if objectif.get_evaluation_mi_annuelle() else '',
            'evaluation_annuelle': objectif.get_evaluation_annuelle() if objectif.get_evaluation_annuelle() else '',
            'notation_manager': objectif.get_notation_manager_display() if objectif.get_notation_manager_display() else '',
            'notation_manager_value': objectif.get_notation_manager() if objectif.get_notation_manager() else 0,
        }
        data_objectifs.append(objectif)
    fiche = {
        'id': fiche_objectif.id,
        'employe': fiche_objectif.get_employe(),
        'bonus': fiche_objectif.get_bonus() if fiche_objectif.get_bonus() else '',
        'commentaire_manager': fiche_objectif.get_commentaire_manager() if fiche_objectif.get_commentaire_manager else '',
        'commentaire_employe': fiche_objectif.get_commentaire_employe() if fiche_objectif.get_commentaire_employe() else ''
    }
    return data_objectifs, fiche


class EvaluationView(TemplateView):
    template_name = 'Fiche_Evaluation/evaluation'

    def get_template_mi_annuelle(self):
        self.template_name += '_mi_annuelle.html'

    def get_template_annuelle(self):
        self.template_name += '_annuelle.html'

    def get(self, request, fiche_id, *args, **kwargs):
        fiche_objectif = get_object_or_404(FicheObjectif, pk=fiche_id)

        # if request.user.is_consultant:
        #    return HttpResponseForbidden()

        if not request.user.is_superieur_to(fiche_objectif.get_employe()):
            return HttpResponseForbidden()

        if get_accessibilite_evaluation_annuelle():  # Reminder to change the month condition to 6
            form = EvaluationAnnuelleForm
            self.get_template_annuelle()
        elif get_accessibilite_evaluation_mi_annuelle():  # Reminder to change the month condition to 12
            form = EvaluationMiAnnuelleForm
            self.get_template_mi_annuelle()
        else:
            return HttpResponseForbidden()

        data_objectifs, fiche = load_fiche_data(fiche_objectif)

        return render(request, template_name=self.template_name,
                      context={'objectifs': data_objectifs, 'fiche': fiche, 'form': form})

    def post(self, request, fiche_id, *args, **kwargs):
        fiche_objectif = FicheObjectif.objects.get(id=fiche_id)
        if get_accessibilite_evaluation_mi_annuelle():                       # Reminder to Change month value to 6
            form = EvaluationMiAnnuelleForm(request.POST or None)
        if get_accessibilite_evaluation_annuelle():  # Reminder to Change month value to 12
            form = EvaluationAnnuelleForm(request.POST or None)
            fiche_objectif.date_validation_manager = now().date()
        else:
            form = None
        if form and form.is_valid():
            try:
                notification = Notification(content_object=fiche_objectif, no_reply=True,
                                            receiver=fiche_objectif.get_employe())
                notification.set_sender(request.user)
                notification.set_subject("Votre fiche d'objectif a été évaluée")
                notification.set_message("Evaluée par %s" % (notification.get_sender().get_full_name()))
                notification.save()
                messages.success(request, "Fiche d'objectif évaluée avec succès")
            except ValueError:
                messages.error(request, "Une erreur est survenue")
                return HttpResponseRedirect(self.request.path_info)
            objectifs = fiche_objectif.get_objectifs()
            notations = request.POST.getlist('notation_manager[]')
            bonus_individuels = []
            for i, objectif in enumerate(objectifs):
                objectif = Objectif.objects.get(id=objectif['id'])
                if type(form) == EvaluationMiAnnuelleForm:
                    objectif.set_evaluation_mi_annuelle(request.POST.get('evaluation_mi_annuelle' + str(i + 1)))
                elif type(form) == EvaluationAnnuelleForm:
                    objectif.set_notation_manager(notations[i])
                    objectif.set_evaluation_annuelle(request.POST.get('evaluation_annuelle' + str(i + 1)))
                    bonus_individuels.append(
                        round(float(objectif.get_notation_manager()) * float(objectif.get_poids()), 2))
                objectif.save()
            fiche_objectif.bonus = sum(bonus_individuels)
            fiche_objectif.save()
        else:
            messages.error(request, "Echèc pendant l'évaluation de la fiche")

        return HttpResponseRedirect(self.request.path_info)


class ConsultationObjectifsView(TemplateView):
    template_name = 'Fiche_Evaluation/consultation_objectifs.html'

    def get(self, request, *args, **kwargs):
        # if request.user.is_consultant:
        #    return HttpResponseForbidden()
        fiches_of_user = FicheObjectif.objects.filter(employe=request.user).values()
        for fiche in fiches_of_user:
            fiche_objectif = FicheObjectif.objects.get(id=fiche['id'])
            if fiche_objectif.is_current:
                data_objectifs, fiche = load_fiche_data(fiche_objectif)
                return render(request, self.template_name,
                              context={'fiche': fiche_objectif, 'objectifs': data_objectifs})
        return render(request, self.template_name)


class ConsultationObjectifsSuperieurView(TemplateView):
    template_name = 'Fiche_evaluation/consultation_objectifs_superieur.html'

    def get(self, request,fiche_id, *args, **kwargs):
        fiche_objectif = get_object_or_404(FicheObjectif, pk=fiche_id)
        if not request.user.is_superieur_to(fiche_objectif.get_employe()):
            return HttpResponseForbidden()

        data_objectifs, fiche = load_fiche_data(fiche_objectif)
        return render(request, self.template_name,
                              context={'fiche': fiche_objectif, 'objectifs': data_objectifs})



def set_commentaire_employe(request):
    fiche_objectif = get_object_or_404(FicheObjectif, pk=request.POST.get('fiche_id'))
    if request.user != fiche_objectif.get_employe():
        return HttpResponseForbidden()
    try:
        fiche_objectif.commentaire_employe = request.POST.get('commentaire_employe')
        fiche_objectif.save()
        return JsonResponse({'Response': 'success'})
    except ValueError:
        return JsonResponse({'Response': 'error'})


def set_commentaire_manager(request):
    fiche_objectif = get_object_or_404(FicheObjectif, pk=request.POST.get('fiche_id'))
    if request.user != fiche_objectif.get_employe().get_superieur_hierarchique():
        return HttpResponseForbidden()
    try:
        fiche_objectif.commentaire_manager = request.POST.get('commentaire_employe')
        fiche_objectif.save()
        return JsonResponse({'Response': 'success'})
    except ValueError:
        return JsonResponse({'Response': 'error'})
