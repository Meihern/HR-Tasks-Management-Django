from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import TemplateView
from .utils import render_to_pdf, get_template, get_template_name, get_month_name, get_banque
from Gestion_Attestations.models import DemandeAttestation, Salaire
from Authentification.models import Departement
import datetime


# Create your views here.


class GeneratePDF(TemplateView):
    template_name = 'Pdfs'

    def get(self, request, *args, **kwargs):
        if not request.user.can_consult_attestations:
            return HttpResponseForbidden()
        if request.session['doc_id']:
            doc_id = request.session['doc_id']
            del request.session['doc_id']
            demande_doc = DemandeAttestation.objects.get(id=doc_id)
            demande_doc_type = get_template_name(demande_doc.get_type_demande())
            self.template_name = self.template_name + '/' + get_template_name(demande_doc_type) + '.html'
            employe = demande_doc.get_employe()
            context = {
                'date': demande_doc.get_date_validation(),
                'sexe': employe.get_sexe_nomination(),
                'nom_prenom': employe.get_full_name(),
                'num_cnss': employe.get_n_cnss(),
                'date_entree': employe.get_date_entree(),
                'fonction': employe.get_fonction(),
                'directeur_rh': Departement.objects.safe_get(id=5).get_directeur().get_full_name(),
                'salaire': Salaire.objects.safe_get(matricule_paie=employe),
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
