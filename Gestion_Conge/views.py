from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseForbidden, Http404, JsonResponse
from Notifications.models import Notification
from Authentification.models import Departement, Activite, Employe
from .models import DemandeConge
from .forms import DemandeCongeForm
from django.core.mail import send_mail
from Realisation.settings import DEFAULT_FROM_EMAIL
from django.template import loader


# Create your views here.

def get_email_context(employe: Employe, demande_conge: DemandeConge, request):
    context = {
        'site_name': 'EMID Digitalisation Services RH',
        'employe': employe,
        'demande_conge': demande_conge,
        'date_envoi': demande_conge.get_date_envoi(),
        'protocol': 'http',
    }
    return context


class DemandeCongeView(FormView):
    form = DemandeCongeForm
    template_name = 'Gestion_Conge/demandeconge.html'
    success_url = '/conges/demande_conge'

    def get(self, request, matricule_employe=None, *args, **kwargs):
        # if request.user.is_consultant:
        #    return HttpResponseForbidden()
        if matricule_employe is not None:
            employe = get_object_or_404(Employe, pk=matricule_employe)
            if request.user != employe.get_superieur_hierarchique():
                return HttpResponseForbidden()
        return render(request, template_name=self.template_name, context={'form': self.form})

    def post(self, request, matricule_employe=None, *args, **kwargs):
        form = self.form(request.POST or None)
        if matricule_employe is not None:
            employe = get_object_or_404(Employe, pk=matricule_employe)
        else:
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
                    context = get_email_context(employe, demande_conge, request)
                    context['domain'] = request.META['HTTP_HOST']
                    email = loader.render_to_string('Gestion_Conge/email_demande_conge.html', context)
                    messages.success(request, "Vote Demande de Congé a été envoyé avec succès")
                except ValidationError:
                    demande_conge.delete()
                    result = self.form_invalid(form)
                    messages.error(request, "Echec de l'envoi de votre demande de congé")
                    return result
                send_mail(notification.get_subject(), email, from_email=DEFAULT_FROM_EMAIL,
                          recipient_list=[notification.get_receiver().get_email()], fail_silently=True)
                return result
            else:
                result = self.form_invalid(form)
                messages.error(request, str(form.errors))
                return result
        else:
            return HttpResponseForbidden()


def accept_demande_conge(request):
    notification_id = request.POST.get('notif_id')
    employe = request.user

    if notification_id:
        notification = Notification.objects.get(id=notification_id)
        demande_conge = notification.get_content_object()
        if not request.user == notification.get_receiver():
            return HttpResponseForbidden()
    else:
        return JsonResponse({'Response': 'error'})

    if not notification.get_receiver() == employe:
        return HttpResponseForbidden()

    try:

        if Departement.objects.filter(directeur=employe.get_superieur_hierarchique()).exists():
            demande_conge.update_etat(DemandeConge.ETAT_SUPERIEUR_HIERARCHIQUE)

        if Departement.objects.filter(directeur=employe).exists():
            demande_conge.update_etat(DemandeConge.ETAT_DIRECTION_CONCERNEE)

        if employe == Departement.objects.safe_get(id=5).get_directeur():
            demande_conge.update_etat(DemandeConge.ETAT_DIRECTION_RH)

        demande_conge = DemandeConge.objects.safe_get(id=demande_conge.get_id())

        if demande_conge.get_etat() == DemandeConge.ETAT_DIRECTION_RH:
            no_reply = True
        else:
            no_reply = False

        notification = Notification(content_object=demande_conge, no_reply=no_reply)
        notification.set_sender(employe)
        notification.set_receiver()
        if no_reply is False:
            notification.set_subject("Demande de Congé")
            notif_msg = str(demande_conge)
        else:
            notification.set_subject("Une nouvelle sur votre demande de congé")
            notif_msg = "Votre demande de congé a été acceptée"
        notification.set_message(notif_msg)
        notification.save()
        context = get_email_context(employe, demande_conge, request)
        context['domain'] = request.META['HTTP_HOST']
    except ValueError:
        return JsonResponse({'Response': 'error'})
    if demande_conge.get_etat() == DemandeConge.ETAT_DIRECTION_RH:
        email = loader.render_to_string("Gestion_Conge/email_accept_demande_conge.html", context)
    else:
        email = loader.render_to_string("Gestion_Conge/email_demande_conge.html")
    send_mail(notification.get_subject(), email, from_email=DEFAULT_FROM_EMAIL,
              recipient_list=[notification.get_receiver().get_email()], fail_silently=True)
    return JsonResponse({'Response': 'success'})


def refuser_demande_conge(request):
    notification_id = request.POST.get('notif_id')
    employe = request.user
    if notification_id:
        notification = Notification.objects.get(id=notification_id)
        demande_conge = notification.get_content_object()
        motif_refus = request.POST.get('motif_refus')
        if not request.user == notification.get_receiver():
            return HttpResponseForbidden()
    else:
        return JsonResponse({'Response': 'error'})

    if not notification.get_receiver() == employe:
        return HttpResponseForbidden()

    try:
        demande_conge.update_etat(DemandeConge.ETAT_REFUS)
        demande_conge.set_motif_refus(motif_refus)
        demande_conge = DemandeConge.objects.safe_get(id=demande_conge.get_id())
        notification = Notification(content_object=demande_conge)
        notification.set_subject("Une nouvelle sur votre demande de congé")
        notification.set_sender(employe)
        notification.set_receiver()
        notification.set_message(
            "Votre demande de Congé a été refusée pour le motif suivant : %s" % (demande_conge.get_motif_refus()))
        notification.save()
        context = get_email_context(employe, demande_conge, request)
        context['domain'] = request.META['HTTP_HOST']
        email = loader.render_to_string("Gestion_Conge/email_refuser_demande_conge.html", context)
    except ValueError:
        return JsonResponse({'Response': 'error'})
    send_mail(notification.get_subject(), email, from_email=DEFAULT_FROM_EMAIL,
              recipient_list=[notification.get_receiver().get_email()], fail_silently=True)
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
            elif request.user.can_consult_shared_tabac_fmcg:
                demandes_conges = DemandeConge.objects.exclude(employe__activite=activite_mdlz).order_by('-date_envoi')
                demandes_conges = demandes_conges.all().values('id', 'employe', 'date_envoi',
                                                               'date_depart', 'date_retour', 'etat')
            elif request.user.can_consult_shared:
                demandes_conges = DemandeConge.objects.all().order_by('-date_envoi')
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
                    'etat_code': demande['etat']
                }
                data.append(demande_conge)
            return render(request, template_name=self.template_name, context={'demandes': data})
        else:
            return HttpResponseForbidden()


def load_data(employe: Employe):
    if employe.can_consult_conges:
        activite_mdlz = Activite.objects.safe_get(id=5)
        if employe.can_consult_mdlz:
            demandes_conges = DemandeConge.objects.filter(employe__activite=activite_mdlz).order_by('-date_envoi')
        elif employe.can_consult_shared_tabac_fmcg:
            demandes_conges = DemandeConge.objects.exclude(employe__activite=activite_mdlz).order_by('-date_envoi')
        elif employe.can_consult_shared:
            demandes_conges = DemandeConge.objects.all().order_by('-date_envoi')

    else:

        related_demandes_notifications = Notification.objects.filter(receiver=employe,
                                                                     content_type=ContentType.objects.get_for_model(
                                                                         DemandeConge))
        notification_objects_ids = list(related_demandes_notifications.all().values('object_id', ))
        demandes_conges_ids = []

        for object in notification_objects_ids:
            demandes_conges_ids.append(object['object_id'])

        demandes_conges = DemandeConge.objects.filter(pk__in=demandes_conges_ids).order_by('-date_envoi')

    demandes_conges = demandes_conges.all().values('id', 'employe', 'date_depart', 'date_retour')

    data_in_conge = []
    data_upcoming_conge = []

    for demande in demandes_conges:
        employe_is_in_conge = DemandeConge.objects.safe_get(id=demande['id']).in_conge
        employe_has_upcoming_conge = DemandeConge.objects.safe_get(id=demande['id']).is_upcoming_conge
        demande_conge = {
            'id': demande['id'],
            'employe': Employe.objects.get(matricule_paie=demande['employe']).get_full_name(),
            'date_depart': demande['date_depart'],
            'date_retour': demande['date_retour'],
        }

        if employe_is_in_conge:
            data_in_conge.append(demande_conge)
        elif employe_has_upcoming_conge:
            data_upcoming_conge.append(demande_conge)
        else:
            pass

    return data_in_conge, data_upcoming_conge


class ConsultationEmployesConges(TemplateView):
    template_name = 'Gestion_Conge/consultation_conges_valides.html'

    def get(self, request, type_conge, *args, **kwargs):

        data_in_conge, data_upcoming_conge = load_data(request.user)

        if type_conge == 'courant':
            return render(request, template_name=self.template_name,
                          context={'demandes': data_in_conge, 'type': type_conge})
        elif type_conge == 'prochain':
            return render(request, template_name=self.template_name,
                          context={'demandes': data_upcoming_conge, 'type': type_conge})
        else:
            return Http404()


class HistoriqueDemandesCongesView(TemplateView):
    template_name = 'Gestion_Conge/historique_demandes_conges.html'

    def get(self, request, *args, **kwargs):
        employe = request.user
        if employe:
            demandes_conges = DemandeConge.objects.filter(employe=employe).order_by('-date_envoi')
            demandes_conges = demandes_conges.all().values('id', 'date_envoi', 'date_depart', 'date_retour', 'etat')
            data = []
            for demande in demandes_conges:
                demande_doc = {
                    'id': demande['id'],
                    'date_envoi': demande['date_envoi'],
                    'etat': DemandeConge.objects.safe_get(id=demande['id']).get_etat_display(),
                    'date_retour': demande['date_retour'],
                    'date_depart': demande['date_depart'],
                    'etat_code': demande['etat']
                }
                data.append(demande_doc)
            return render(request, template_name=self.template_name, context={'demandes_conges': data})
        else:
            return HttpResponseForbidden()
