from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, Http404
from .models import DemandeAttestation, TypeDemandeAttestation
from Notifications.models import Notification
from Authentification.models import Activite
from django.views.generic import TemplateView
from Authentification.models import Employe
from django.core.mail import send_mail
from Realisation.settings import DEFAULT_FROM_EMAIL


# Create your views here.


class DemandeAttestationView(TemplateView):
    template_name = 'Gestion_Attestations/demande_attestation.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


def envoyer_demande_doc(request):
    employe = request.user
    type_demande = request.POST.get("type_demande")
    if type_demande:
        # if employe.is_consultant:
        #   return HttpResponseForbidden()
        type_demande = TypeDemandeAttestation.objects.get(nom_type_demande=type_demande)
        demande_doc = DemandeAttestation(employe=employe, type=type_demande)
        try:
            demande_doc.save()
            notification = Notification(content_object=demande_doc, no_reply=False)
            notification.set_subject(str(type_demande))
            notification.set_message(str(demande_doc))
            notification.set_sender(employe)
            notification.set_receiver()
            notification.save()
        except ValueError:
            demande_doc.delete()
            return JsonResponse({'Response': 'error'})
        send_mail(notification.get_subject(), notification.get_message(),
                  from_email=DEFAULT_FROM_EMAIL, recipient_list=[notification.get_receiver().get_email()], fail_silently=True)
        return JsonResponse({'Response': 'Success'})
    else:
        return JsonResponse({'Response': 'error'})


def envoyer_demande_doc_superieur(request, matricule_employe):
    type_demande = request.POST.get("type_demande")
    if type_demande:
        type_demande = TypeDemandeAttestation.objects.get(nom_type_demande=type_demande)
        employe = get_object_or_404(Employe, pk=matricule_employe)
        demande_doc = DemandeAttestation(employe=employe, type=type_demande)
        try:
            demande_doc.save()
            notification = Notification(content_object=demande_doc, no_reply=False)
            notification.set_subject(str(type_demande))
            notification.set_message(str(demande_doc))
            notification.set_sender(request.user)
            notification.set_receiver()
            notification.save()
        except ValueError:
            demande_doc.delete()
            return JsonResponse({'Response': 'error'})
        send_mail(notification.get_subject(), notification.get_message(),
                  from_email=DEFAULT_FROM_EMAIL, recipient_list=[notification.get_receiver().get_email()], fail_silently=True)
        return JsonResponse({'Response': 'success'})
    else:
        return JsonResponse({'Response': 'error'})


def accept_demande_doc(request):
    notif_id = request.POST.get('notif_id')
    doc_id = request.POST.get('doc_id')

    if notif_id:
        notification = get_object_or_404(Notification, pk=notif_id)
        if request.user != notification.get_receiver():
            return HttpResponseForbidden()
        demande_doc = notification.get_content_object()
    elif doc_id:
        if not request.user.can_consult_attestations:
            return HttpResponseForbidden()
        demande_doc = get_object_or_404(DemandeAttestation, pk=doc_id)
    else:
        return JsonResponse({'Response': 'error'})
    demande_doc.update_etat_validation()
    notification = Notification(sender=request.user, receiver=demande_doc.get_employe(),
                                subject='Nouvelle sur votre ' + str(demande_doc.get_type_demande()),
                                message='Votre demande de %s a été acceptée !' % (demande_doc.get_type_demande()),
                                content_object=demande_doc)
    notification.save()
    send_mail(notification.get_subject(), notification.get_message(),
              from_email=DEFAULT_FROM_EMAIL, recipient_list=[notification.get_receiver().get_email()], fail_silently=True)
    return JsonResponse({'Response': 'success'})


class ConsultationDemandesDoc(TemplateView):
    template_name = 'Gestion_Attestations/consultation_attestations.html'

    def get(self, request, type_doc, *args, **kwargs):

        if request.user.can_consult_attestations:
            activite_mdlz = Activite.objects.safe_get(id=5)
            type_doc = TypeDemandeAttestation.objects.get(nom_type_demande=type_doc)
            if request.user.can_consult_mdlz:
                demandes_docs = DemandeAttestation.objects.filter(type=type_doc,
                                                                  employe__activite=activite_mdlz).order_by(
                    '-date_envoi')
                demandes_docs = demandes_docs.all().values('id', 'type', 'date_envoi', 'etat_validation', 'employe')
            elif request.user.can_consult_shared_tabac_fmcg:
                demandes_docs = DemandeAttestation.objects.filter(type=type_doc).exclude(
                    employe__activite=activite_mdlz).order_by('-date_envoi')
                demandes_docs = demandes_docs.all().values('id', 'type', 'date_envoi', 'etat_validation', 'employe')
            elif request.user.can_consult_shared:
                demandes_docs = DemandeAttestation.objects.filter(type=type_doc).order_by('-date_envoi')
                demandes_docs = demandes_docs.all().values('id', 'type', 'date_envoi', 'etat_validation', 'employe')
            else:
                return HttpResponseForbidden()
            data = []
            for demande in demandes_docs:
                demande_doc = {
                    'id': demande['id'],
                    'type': TypeDemandeAttestation.objects.get(id=demande['type']),
                    'date_envoi': demande['date_envoi'],
                    'employe': Employe.objects.get(matricule_paie=demande['employe']).get_full_name(),
                    'etat': demande['etat_validation'],
                }
                data.append(demande_doc)

            return render(request, template_name=self.template_name, context={'docs': data})
        else:
            return HttpResponseForbidden()


class HistoriqueDemandesAttestationsView(TemplateView):
    template_name = 'Gestion_Attestations/historique_demandes_attestations.html'

    def get(self, request, *args, **kwargs):
        employe = request.user
        if employe:
            demandes_docs = DemandeAttestation.objects.filter(employe=employe)
            demandes_docs = demandes_docs.all().values('id', 'type', 'date_envoi', 'etat_validation')
            data = []
            for demande in demandes_docs:
                demande_doc = {
                    'id': demande['id'],
                    'type': TypeDemandeAttestation.objects.get(id=demande['type']),
                    'date_envoi': demande['date_envoi'],
                    'etat': demande['etat_validation'],
                }
                data.append(demande_doc)
            return render(request, template_name=self.template_name, context={'docs': data})
        else:
            return HttpResponseForbidden()


class AttestationEquipeView(TemplateView):
    template_name = 'Gestion_Attestations/equipe_demande_attestation.html'

    def get(self, request, employe_id, *args, **kwargs):
        current_employe = get_object_or_404(Employe, pk=employe_id)
        if current_employe.get_superieur_hierarchique() != request.user:
            return HttpResponseForbidden()
        return render(request, self.template_name, context={'nom_prenom': current_employe.get_full_name(),
                                                            'matricule': employe_id})