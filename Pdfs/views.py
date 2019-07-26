from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView,View
from django.utils import timezone
from Authentification.models import Employe
from Gestion_Attestations.models import DemandeAttestation
# Create your views here.
from .utils import render_to_pdf, get_template
from Realisation.settings import MEDIA_ROOT

class GeneratePDF(TemplateView):
    template_name = 'Pdfs/attestationdetravail.html'
    def get(self, request, *args, **kwargs):
        employe = Employe.objects.get(id=request.user.id)
        template = get_template(self.template_name)
        context = {
            "date": timezone.now(),
            "nom_prenom": employe.get_full_name(),
            "num_cnss": employe.get_n_cnss(),
            "date_entree": employe.get_date_entree(),
            "fonction": employe.get_fonction(),
            "directeur_rh": Employe.objects.get(fonction="DIRECTEUR RESSOURCES HUMAINES").get_full_name()
        }
        html = template.render(context)
        pdf = render_to_pdf(self.template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "attesation_travail_%s.pdf" %(employe.get_full_name())
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
