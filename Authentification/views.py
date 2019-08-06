from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django import forms
from django.contrib.auth import (
    forms,
    views,
    logout,
    authenticate,
    login,
    get_user_model,
    password_validation
)
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.mail import send_mail

from Gestion_Attestations.models import Salaire
from . import forms
from Realisation.settings import LOGIN_REDIRECT_URL, LOGIN_URL, DEFAULT_FROM_EMAIL

# Create your views here.


Employe = get_user_model()


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(LOGIN_REDIRECT_URL)


class AuthenticationView(TemplateView,views.LoginView):
    template_name = 'Authentification/login.html'
    form = forms.LoginForm()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST or None)
        if form.is_valid():
            matricule_paie = form.cleaned_data.get('matricule_paie')
            password = form.cleaned_data.get('password')
            employe = authenticate(request, username=matricule_paie, password=password)
            if employe is not None:
                login(request, employe)
                return HttpResponseRedirect(LOGIN_REDIRECT_URL)
            else:
                messages.error(request,"Authentification Echouée, Adresse Electronique ou Mot de Passe Incorrecte")
                return HttpResponseRedirect(LOGIN_URL)
        else:
            messages.error(request, "Formulaire Invalide")
            return render(request, self.template_name, {'form': self.form})


class SendPasswordResetEmail(FormView):

    template_name = 'Authentification/send_email_password_change.html'
    form = forms.SendPasswordResetEmailForm
    success_url = LOGIN_URL

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            matricule_paie = form.cleaned_data.get('matricule_paie')
            employe = Employe.objects.safe_get(matricule_paie=matricule_paie)
            if employe:
                try:
                    validate_email(employe.get_email())
                except ValidationError:
                    messages.error(request, " Votre Email est invalide ")
                context = {
                    'email': employe.get_email(),
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'Digitalisation Services RH',
                    'uid': urlsafe_base64_encode(force_bytes(employe.get_matricule())),
                    'user': employe,
                    'token': default_token_generator.make_token(employe),
                    'protocol': 'http',
                }
                subject_template_name = 'Authentification/password_reset_subject.txt'
                email_template_name = 'Authentification/password_reset_email.html'
                subject = loader.render_to_string(subject_template_name, context)
                subject = ''.join(subject.splitlines())
                email = loader.render_to_string(email_template_name, context)
                send_mail(subject, email, DEFAULT_FROM_EMAIL, [employe.get_email()], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Un message éléctronique a été envoyé à '
                                 + employe.get_email() + ". Veuillez vérifier votre boîte de messagerie "
                                                         "pour changer votre mot de passe .")
                return result
            else:
                result = self.form_invalid(form)
                messages.error(request, "Matricule n'existe pas ")
                return result


class ResetPasswordView(FormView):

    template_name = 'Authentification/password_change.html'
    form_class = forms.ChangePasswordForm
    success_url = LOGIN_URL

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        form = self.form_class(request.POST or None)
        UserModel = get_user_model()
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            employe = UserModel._default_manager.get(pk=uid)
            print(employe)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            employe = None
        if employe is not None and default_token_generator.check_token(employe, token):
            if form.is_valid():
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')
                if new_password1 == new_password2:
                    try:
                        password_validation.validate_password(new_password1)
                    except password_validation.ValidationError as e:
                        messages.error(request, e)
                        return self.form_invalid(form)
                    employe.set_password(new_password1)
                    employe.save()
                    messages.success(request, "Votre mot de passe a été modifié avec succès")
                    return self.form_valid(form)
                else:
                    messages.error(request, "Les deux mots de passes saisis sont différents")
                    return self.form_invalid(form)
            else:
                messages.error(request, "Changement de Mot de Passe échouée ")
                return self.form_invalid(form)
        else:
            messages.error(request, "Le lien de changement de mot de passe n'est plus valide")
            return self.form_invalid(form)


class ProfileView(TemplateView):
    template_name = 'Authentification/profile.html'

    def get(self, request, *args, **kwargs):
        employe = request.user
        if employe:
            context = {
                'name': employe.get_full_name(),
                'Matricule': employe.get_matricule(),
                'Fonction': employe.get_fonction(),
                'salaire': Salaire.objects.safe_get(matricule_paie=employe),
                'cnss': employe.get_n_cnss(),
                'Departement': employe.get_departement(),
            }

            return render(request, template_name=self.template_name, context=context)
        else:
            return HttpResponseForbidden()


class HistoriqueDemandesView(TemplateView):
    template_name = 'Authentification/historique_demandes.html'

    def get(self, request, *args, **kwargs):
        employe = request.user
        if employe:
            '''
            context = {
                'name': employe.get_full_name(),
                'Matricule': employe.get_matricule(),
                'Fonction': employe.get_fonction(),
                'salaire': 2500,#employe.get_salaire(),
                'cnss': employe.get_n_cnss(),
                'Departement': 'Ressources Humaines',#employe.get_departement(),
            }
            '''
            return render(request, template_name=self.template_name)
        else:
            return HttpResponseForbidden()

