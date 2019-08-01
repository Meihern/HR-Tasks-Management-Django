from django.shortcuts import render
import io
from django.http import JsonResponse, HttpResponseForbidden
from .models import DemandeAttestation, TypeDemandeAttestatation
from Notifications.models import Notification
from Authentification.models import Departement
from django.views.generic import TemplateView
from Authentification.models import Employe
# Create your views here.


class DemandeAttestationView(TemplateView):
    template_name = 'Gestion_Attestations/demande_attestation.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


def envoyer_demande_doc(request):
    employe = request.user
    type_demande = request.GET.get("type_demande")
    if type_demande:
        type_demande = TypeDemandeAttestatation.objects.get(nom_type_demande=type_demande)
        demande_doc = DemandeAttestation(employe=employe, type=type_demande)
        demande_doc.save()
        notif_subject = str(type_demande)
        notif_receiver = Departement.objects.get(nom_departement='Ressources Humaines').get_directeur()
        notif_msg = str(demande_doc)
        notification = Notification(sender=employe, receiver=notif_receiver, subject=notif_subject,
                                    message=notif_msg, content_object=demande_doc)
        notification.save()
        return JsonResponse({'Response': 'Success'})
    else:
        return JsonResponse({'Response': 'Failure'})


def accept_demande_doc(request):
    notif_id = request.GET.get('notif_id')
    doc_id = request.GET.get('doc_id')
    if notif_id:
        notification = Notification.objects.get(id=request.GET.get('notif_id'))
        demande_doc = notification.get_content_object()
    elif doc_id:
        demande_doc = DemandeAttestation.objects.get(id=doc_id)
    else:
        return JsonResponse({'Response': 'error'})
    demande_doc.update_etat_validation()
    notification = Notification(sender=request.user, receiver=demande_doc.get_employe(),
                                subject=demande_doc.get_type_demande(), message='Votre demande a été acceptée !', content_object=demande_doc)
    notification.save()
    request.session['doc_id'] = demande_doc.id
    return JsonResponse({'Response': 'success'})


class ConsultationDemandesDoc(TemplateView):
    template_name = 'consultation.html'

    def get(self, request, type_doc, *args, **kwargs):
        directeur_rh = Departement.objects.get(nom_departement='Ressources Humaines').get_directeur()
        if request.user.is_staff:
            type_doc = TypeDemandeAttestatation.objects.get(nom_type_demande=type_doc)
            demandes_docs = DemandeAttestation.objects.filter(type=type_doc).order_by('-date_envoi')
            demandes_docs = demandes_docs.all().values('id', 'type', 'date_envoi', 'etat_validation', 'employe')
            data = []
            for demande in demandes_docs:
                demande_doc = {
                    'id': demande['id'],
                    'type': TypeDemandeAttestatation.objects.get(id=demande['type']),
                    'date_envoi': demande['date_envoi'],
                    'employe': Employe.objects.get(matricule_paie=demande['employe']).get_full_name(),
                    'etat': demande['etat_validation'],
                }
                data.append(demande_doc)

            return render(request, template_name=self.template_name, context={'docs': data})
        else:
            return HttpResponseForbidden()





