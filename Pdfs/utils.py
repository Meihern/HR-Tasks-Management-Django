import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from Realisation import settings
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def fetch_resources(uri, rel):
    print(settings.MEDIA_ROOT)
    print(settings.MEDIA_URL)
    path = os.path.join(settings.MEDIA_ROOT)
    print(path)

    return path
