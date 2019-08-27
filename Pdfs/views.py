from django.http import HttpResponse, HttpResponseForbidden
from django.utils.timezone import now
from django.views.generic import TemplateView

from Fiche_Evaluation.models import FicheObjectif
from Gestion_Conge.models import DemandeConge
from .utils import render_to_pdf, get_template, get_template_name, get_month_name, get_banque
from Gestion_Attestations.models import DemandeAttestation, Salaire
from Authentification.models import Departement
import datetime
from django.shortcuts import get_object_or_404
from Fiche_Evaluation.utils import load_fiche_data
# Create your views here.


class GeneratePDFAttestations(TemplateView):
    template_name = 'Pdfs'

    def get(self, request, doc_id, *args, **kwargs):
        if not request.user.can_consult_attestations:
            return HttpResponseForbidden()
        if doc_id:
            demande_doc = get_object_or_404(DemandeAttestation, pk=doc_id)
            demande_doc_type = get_template_name(demande_doc.get_type_demande())
            self.template_name = self.template_name + '/' + get_template_name(demande_doc_type) + '.html'
            employe = demande_doc.get_employe()
            context = {
                'date': demande_doc.get_date_validation(),
                'sexe': employe.get_sexe_nomination(),
                'sexe_value': employe.sexe,
                'nom_prenom': employe.get_full_name(),
                'num_cnss': employe.get_n_cnss(),
                'date_entree': employe.get_date_entree(),
                'fonction': employe.get_fonction(),
                'directeur_rh': Departement.objects.safe_get(id=5).get_directeur().get_full_name(),
                'salaire': Salaire.objects.safe_get(matricule_paie=employe).get_valeur_brute() if Salaire.objects.safe_get(matricule_paie=employe) else 'Non défini' ,
                'num_compte': employe.get_n_compte(),
                'mois_courant': get_month_name(datetime.datetime.now().month),
                'mois_precedant': get_month_name(datetime.datetime.now().month - 1),
                'bank': get_banque(employe.get_n_compte()),
            }
            if context:
                template = get_template(self.template_name)
                html = template.render(context)
                pdf = render_to_pdf(self.template_name, context)
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "%s_%s.pdf" % (demande_doc_type, context['nom_prenom'].replace(' ', '_'))
                    content = "inline; filename=%s" % filename
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename=%s" % filename
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not found")
            else:
                return HttpResponse("No context")
        else:
            return HttpResponseForbidden()


class GeneratePDFFichesObjectifs(TemplateView):
    template_name = 'Pdfs/fiche_evaluation.html'

    def get(self, request, fiche_id, *args, **kwargs):
        fiche_objectif = get_object_or_404(FicheObjectif, pk=fiche_id)
        if fiche_objectif.get_employe() != request.user and fiche_objectif.get_employe().get_superieur_hierarchique() != request.user:
            return HttpResponseForbidden()
        objectifs = load_fiche_data(fiche_objectif)[0]
        employe = fiche_objectif.get_employe()
        context = {
            'matricule': employe.get_matricule(),
            'nom_prenom': employe.get_full_name(),
            'fonction': employe.get_fonction(),
            'departement': employe.get_departement(),
            'manager': employe.get_superieur_hierarchique().get_full_name(),
            'fonctionM': employe.get_superieur_hierarchique().get_fonction(),
            'periode': now().date().year,
            'bonus': int(fiche_objectif.get_bonus()*100),
            'commentaire_manager': fiche_objectif.get_commentaire_manager() if fiche_objectif.get_commentaire_manager() else '',
            'commentaire_employe': fiche_objectif.get_commentaire_employe() if fiche_objectif.get_commentaire_employe() else '',
            'date_commentaire_employe': fiche_objectif.get_date_validation_employe() if fiche_objectif.get_date_validation_employe() else '',
            'date_commentaire_manager': fiche_objectif.get_date_validation_manager() if fiche_objectif.get_date_validation_manager() else '',
            'objectifs': objectifs
        }
        if context:
            template = get_template(self.template_name)
            html = template.render(context)
            pdf = render_to_pdf(self.template_name, context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "FicheObjectif_%s.pdf" % (context['nom_prenom'].replace(' ', '_'))
                content = "inline; filename=%s" % filename
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" % filename
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
        else:
            return HttpResponse("No context")


class GeneratePDFDemandeConge(TemplateView):
    template_name = 'Pdfs/demandeconge.html'

    def get(self, request, demande_conge_id, *args, **kwargs):
        demande_conge = get_object_or_404(DemandeConge, pk=demande_conge_id)
        if demande_conge.get_employe() != request.user and not request.user.can_consult_conges:
            return HttpResponseForbidden()
        employe = demande_conge.get_employe()
        context = {
            'matricule': employe.get_matricule(),
            'nom_prenom': employe.get_full_name(),
            'departement': employe.get_departement(),
            'ville': employe.ville,
            'date_depart': demande_conge.get_date_depart(),
            'date_retour': demande_conge.get_date_retour(),
            'jours_ouvrables': demande_conge.get_jours_ouvrables(),
            'telephone': demande_conge.get_telephone() if demande_conge.get_telephone() else 'Aucun',
            'interim': demande_conge.get_interim() if demande_conge.get_interim() else 'Aucun',
            'date_demande': demande_conge.get_date_envoi(),
            'date_validation_superieur': demande_conge.get_date_sup() if demande_conge.get_date_sup() else '',
            'date_validation_direction': demande_conge.get_date_direction() if demande_conge.get_date_direction() else '',
            'date_validation_direction_rh': demande_conge.get_date_direction_rh() if demande_conge.get_date_direction_rh() else '',
            'annee_courante': now().year
        }
        if context:
            template = get_template(self.template_name)
            html = template.render(context)
            pdf = render_to_pdf(self.template_name, context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "DemandeConge_%s.pdf" % (context['nom_prenom'].replace(' ', '_'))
                content = "inline; filename=%s" % filename
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" % filename
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
        else:
            return HttpResponse("No context")




