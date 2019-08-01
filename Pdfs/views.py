from django.http import HttpResponse
from django.views.generic import TemplateView
from .utils import render_to_pdf, get_template,get_template_name, get_month_name
from Gestion_Attestations.models import DemandeAttestation
from Authentification.models import Departement, Salaire
import datetime
# Create your views here.


class GeneratePDF(TemplateView):
    template_name = 'Pdfs'

    def get(self, request, *args, **kwargs):
        doc_id = request.session['doc_id']
        del request.session['doc_id']
        demande_doc = DemandeAttestation.objects.get(id=doc_id)
        demande_doc_type = get_template_name(demande_doc.get_type_demande())
        self.template_name = self.template_name+'/'+get_template_name(demande_doc_type)+'.html'
        employe = demande_doc.get_employe()
        context = {
            'date': demande_doc.get_date_validation() or None,
            'nom_prenom': employe.get_full_name() or None,
            'num_cnss': employe.get_n_cnss() or None,
            'date_entree': employe.get_date_entree() or None,
            'fonction': employe.get_fonction() or None,
            'directeur_rh': Departement.objects.get(nom_departement='Ressources Humaines').get_directeur().get_full_name() or None,
            'salaire': Salaire.objects.get(matricule_paie=employe).get_valeur_brute() or None,
            'num_compte': employe.get_n_compte() or None,
            'mois':  get_month_name(datetime.datetime.now().month),
            'bank': 'CIH',
        }
        if context:
            template = get_template(self.template_name)
            html = template.render(context)
            pdf = render_to_pdf(self.template_name, context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "%s_%s.pdf" %(demande_doc_type,context['nom_prenom'])
                content = "inline; filename='%s'" %(filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" %(filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
        else:
            return HttpResponse("No context")

