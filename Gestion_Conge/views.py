from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseForbidden, Http404, JsonResponse
from Notifications.models import Notification
from Authentification.models import Departement, Activite, Employe
from .models import DemandeConge
from .forms import DemandeCongeForm
from django.core.mail import send_mail
from Realisation.settings import DEFAULT_FROM_EMAIL


# Create your views here.


class DemandeCongeView(FormView):
    form = DemandeCongeForm
    template_name = 'Gestion_Conge/demandeconge.html'
    success_url = '/conges/demande_conge'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        employe = request.user
        if employe:
            if form.is_valid():
                result = self.form_valid(form)
                date_depart = form.cleaned_data.get('date_depart')
                date_retour = form.cleaned_data.get('date_retour')
                jours_ouvrables = form.cleaned_data.get('jours_ouvrables')
                interim = form.cleaned_data.get('interim')
                telephone = form.cleaned_data.get('telephone')
                demande_conge = DemandeConge(employe=employe, date_depart=date_depart,
                                             date_retour=date_retour, interim=interim, telephone=telephone,
                                             jours_ouvrables=jours_ouvrables)
                demande_conge.save()
                try:
                    notification = Notification(content_object=demande_conge, no_reply=False)
                    notification.set_subject("Demande de Congé")
                    notification.set_message(str(demande_conge))
                    notification.set_sender(employe)
                    notification.set_receiver()
                    notification.save()
                    # send_mail(notif_subject, notif_msg, from_email=DEFAULT_FROM_EMAIL,
                    #          recipient_list=[notif_receiver.get_email()])
                    messages.success(request, "Vote Demande de Congé a été envoyé avec succés")
                except:
                    result = self.form_invalid(form)
                    messages.error(request, "Echec de l'envoi de votre demande de congé")
                return result
            else:
                result = self.form_invalid(form)
                messages.error(request, str(form.errors))
                return result
        else:
            return HttpResponseForbidden()


def accept_demande_conge(request):
    notification_id = request.GET.get('notif_id')
    employe = request.user

    if notification_id:
        notification = Notification.objects.get(id=notification_id)
        demande_conge = notification.get_content_object()
        if not request.user == notification.get_receiver():
            return HttpResponseForbidden()
    else:
        return JsonResponse({'Response': 'error'})

    try:

        if employe.get_superieur_hierarchique() == demande_conge.get_employe().get_departement().get_directeur():
            demande_conge.update_etat(DemandeConge.ETAT_SUPERIEUR_HIERARCHIQUE)

        if employe == demande_conge.get_employe().get_departement().get_directeur():
            demande_conge.update_etat(DemandeConge.ETAT_DIRECTION_CONCERNEE)

        if employe == Departement.objects.safe_get(id=5).get_directeur():
            demande_conge.update_etat(DemandeConge.ETAT_DIRECTION_RH)

        demande_conge = DemandeConge.objects.safe_get(id=demande_conge.get_id())

        if demande_conge.get_etat() == DemandeConge.ETAT_DIRECTION_RH:
            no_reply = True
        else:
            no_reply = False

        notification = Notification(content_object=demande_conge, no_reply=no_reply)
        notification.set_subject("Demande de Congé")
        notification.set_sender(employe)
        notification.set_receiver()
        if no_reply is False:
            notif_msg = str(demande_conge)
        else:
            notif_msg = "Votre demande de congé a été acceptée"
        notification.set_message(notif_msg)
        notification.save()
        ''' Uncomment to apply sending emails
        send_mail(notification.get_subject(), notification.get_message(), from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=[notification.get_receiver()])
        '''
    except ValueError:
        return JsonResponse({'Response': 'error'})

    return JsonResponse({'Response': 'success'})


def refuser_demande_conge(request):
    notification_id = request.GET.get('notif_id')
    employe = request.user
    if notification_id:
        notification = Notification.objects.get(id=notification_id)
        demande_conge = notification.get_content_object()
        if not request.user == notification.get_receiver():
            return HttpResponseForbidden()
    else:
        return JsonResponse({'Response': 'error'})

    try:
        demande_conge.update_etat(DemandeConge.ETAT_REFUS)
        demande_conge = DemandeConge.objects.safe_get(id=demande_conge.get_id())
        notification = Notification(content_object=demande_conge)
        notification.set_subject("Demande de Congé")
        notification.set_sender(employe)
        notification.set_receiver()
        notification.set_message("Votre demande de Congé a été refusée")
        notification.save()
        # send_mail(notif_subject, notif_msg, from_email=DEFAULT_FROM_EMAIL,
        #          recipient_list=[notif_receiver.get_email()])
    except ValueError:
        return JsonResponse({'Response': 'error'})

    return JsonResponse({'Response': 'success'})


class ConsultationDemandeConges(TemplateView):
    template_name = "Gestion_Conge/consultation_conges.html"


    def get(self, request, *args, **kwargs):
        if request.user.can_consult_conges:
            activite_mdlz = Activite.objects.safe_get(id=5)
            if request.user.can_consult_mdlz:
                demandes_conges = DemandeConge.objects.filter(employe__activite=activite_mdlz).order_by('-date_envoi')
                demandes_conges = demandes_conges.all().values('id', 'employe', 'date_envoi',
                                                               'date_depart', 'date_retour', 'etat')
            elif request.user.can_consult_shared:
                demandes_conges = DemandeConge.objects.exclude(employe__activite=activite_mdlz).order_by('-date_envoi')
                demandes_conges = demandes_conges.all().values('id', 'employe', 'date_envoi',
                                                               'date_depart', 'date_retour', 'etat')
            else:
                return HttpResponseForbidden()
            data = []
            for demande in demandes_conges:
                demande_conge = {
                    'id': demande['id'],
                    'date_envoi': demande['date_envoi'],
                    'employe': Employe.objects.get(matricule_paie=demande['employe']).get_full_name(),
                    'etat': DemandeConge.objects.safe_get(id=demande['id']).get_etat_display(),
                    'date_depart': demande['date_depart'],
                    'date_retour': demande['date_retour'],
                }
                data.append(demande_conge)
            return render(request, template_name=self.template_name, context={'demandes': data})
        else:
            return HttpResponseForbidden()
