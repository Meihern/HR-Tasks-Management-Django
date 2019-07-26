from django.shortcuts import render
import io
from django.http import JsonResponse
from .models import DemandeAttestation, TypeDemandeAttestataion
# Create your views here.


def envoyer_demande_travail(request):
    employe = request.user
    type_demande = TypeDemandeAttestataion.objects.get(nom_type_demande='travail')
    demande_travail = DemandeAttestation(employe=employe, type=type_demande)
    demande_travail.save()
    return JsonResponse({'test': 'test'})

def envoyer_demande_salaire(request):
    employe = request.user
    type_demande = TypeDemandeAttestataion.objects.get(nom_type_demande='salaire')
    demande_travail = DemandeAttestation(employe=employe, type=type_demande)
    demande_travail.save()
    return JsonResponse({'test': 'test'})

def envoyer_demande_domiciliation(request):
    employe = request.user
    type_demande = TypeDemandeAttestataion.objects.get(nom_type_demande='domiciliation')
    demande_travail = DemandeAttestation(employe=employe, type=type_demande)
    demande_travail.save()
    return JsonResponse({'test': 'test'})


def generate_attestation_travail_pdf(request):
    pass



