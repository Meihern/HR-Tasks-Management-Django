from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView,View
from django.utils import timezone
# Create your views here.
from .utils import render_to_pdf,get_template


class GeneratePDF(TemplateView):
    template_name = 'Pdfs/attestationdetravail.html.html'
    def get(self, request, *args, **kwargs):
        template = get_template('Pdfs/attestationdetravail.html.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf(self.template_name)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
