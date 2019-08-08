from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseForbidden, Http404
from Authentification.models import Departement
from Notifications.models import Notification
from .models import DemandeConge
from .forms import DemandeCongeForm
from django.core.mail import send_mail
from Realisation.settings import DEFAULT_FROM_EMAIL
# Create your views here.


class DemandeCongeView(FormView):
    form = DemandeCongeForm
    template_name = 'Gestion_Conge/demandeconge.html'
    success_url = '/conges/demande_conge'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        employe = request.user
        if employe:
            if form.is_valid():
                result = self.form_valid(form)
                date_depart = form.cleaned_data.get('date_depart')
                date_retour = form.cleaned_data.get('date_retour')
                jours_ouvrables = form.cleaned_data.get('jours_ouvrables')
                interim = form.cleaned_data.get('interim')
                telephone = form.cleaned_data.get('telephone')
                demande_conge = DemandeConge(employe=employe, date_depart=date_depart,
                                             date_retour=date_retour, interim=interim, telephone=telephone,
                                             jours_ouvrables=jours_ouvrables)
                demande_conge.save()
                try:
                    notif_subject = "Demande de Congé"
                    notif_msg = str(demande_conge)
                    notif_receiver = demande_conge.get_notif_receiver(DemandeConge.ETAT_ENVOI)
                    notification = Notification(sender=employe, receiver=notif_receiver, subject=notif_subject,
                                            message=notif_msg, content_object=demande_conge, no_reply=False)
                    notification.save()
                    send_mail(notif_subject, notif_msg, from_email=DEFAULT_FROM_EMAIL,
                              recipient_list=[notif_receiver.get_email()])
                    messages.success(request, "Vote Demande de Congé a été envoyé avec succés")
                except:
                    result = self.form_invalid(form)
                    messages.error(request, "Echec de l'envoi de votre demande de congé")
                return result
            else:
                result = self.form_invalid(form)
                messages.error(request, str(form.errors))
                return result
        else:
            return HttpResponseForbidden()


def accept_demande_conge(request):

    notif_id = request.GET.get('notif_id')
    conge_id = request.GET.get('conge_id')
    if notif_id:
        notification = Notification.objects.safe_get(id=notif_id)
        demande_conge = notification.get_content_object()
    elif conge_id:
        demande_conge = DemandeConge.objects.safe_get(id=conge_id)
    else:
        pass

