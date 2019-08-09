import os
import pandas as pd
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from Realisation import settings


def get_month_name(month: int):

    if month == 1:
        return 'Janvier'
    if month == 2:
        return 'Février'
    if month == 3:
        return 'Mars'
    if month == 4:
        return 'Avril'
    if month == 5:
        return 'Mai'
    if month == 6:
        return 'Juin'
    if month == 7:
        return 'Juillet'
    if month == 8:
        return 'Août'
    if month == 9:
        return 'Septembre'
    if month == 10:
        return 'Octobre'
    if month == 11:
        return 'Novembre'
    if month == 12:
        return 'Décembre'
    else:
        return None


def get_banque(rib: str = None):
    if rib:
        data = pd.read_csv('Pdfs/RIBS_banques.csv', sep=",", names=['Code', 'Libelle'])
        return data[data.Code == rib[:3]][['Libelle']].to_string(index=False, header=False)
    else:
        return None


def get_template_name(doc_type: str):

    if 'travail' in str(doc_type):
        return 'attestationdetravail'

    if 'domiciliation' in str(doc_type):
        return 'domiciliationdesalaire'

    if 'salaire' in str(doc_type):
        return 'attestationdesalaire'


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path
