from django.shortcuts import render
import io
from django.http import JsonResponse
from .models import DemandeAttestation, TypeDemandeAttestataion
from Notifications.models import Notification
from Authentification.models import Employe, Departement
# Create your views here.


def envoyer_demande_doc(request):
    employe = request.user
    type_demande = request.GET.get("type_demande")
    if type_demande:
        type_demande = TypeDemandeAttestataion.objects.get(nom_type_demande=type_demande)
        demande_travail = DemandeAttestation(employe=employe, type=type_demande)
        demande_travail.save()
        notif_subject = str(type_demande)
        notif_receiver = Departement.objects.get(nom_departement='Ressources Humaines').get_directeur()
        notif_msg = str(demande_travail)
        notification = Notification(sender=employe, receiver=notif_receiver, subject=notif_subject, message=notif_msg)
        notification.save()
        return JsonResponse({'Response': 'Sucess'})
    else:
        return JsonResponse({'Response': 'Failure'})






