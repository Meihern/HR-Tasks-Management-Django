from django.shortcuts import render
from django.views.generic import TemplateView
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

from Authentification.models import Salaire
from . import forms
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from Realisation.settings import LOGIN_REDIRECT_URL, LOGIN_URL
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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            employe = authenticate(request, username=email, password=password)
            if employe is not None:
                if employe.last_login is None:
                    request.session['reset_password_stamp'] = True #Allow the employe access to the change password page
                    request.session['reset_password_email'] = email #Storing the sent email temporarily in a session variable
                    return HttpResponseRedirect('reset_password') #Redirecting the Employe to the change password page
                else:
                    login(request, employe)
                    return HttpResponseRedirect(LOGIN_REDIRECT_URL)
            else:
                messages.error(request,"Authentification Echouée, Adresse Electronique ou Mot de Passe Incorrecte")
                return HttpResponseRedirect(LOGIN_URL)
        else:
            return render(request, self.template_name, {'form': self.form})


class ResetPasswordView(TemplateView):

    template_name = 'Authentification/password_change.html'
    form = forms.ChangePasswordForm()

    def get(self, request, *args, **kwargs):
        if 'reset_password_stamp' in request.session:
            del request.session['reset_password_stamp']
            stored_email = request.session['reset_password_email']
            del request.session['reset_password_email']
            return render(request, self.template_name, {'form': self.form,'email': stored_email})
        else:
            return HttpResponseRedirect(LOGIN_URL)

    def post(self, request, *args, **kwargs):
        form = forms.ChangePasswordForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            old_password = form.cleaned_data.get('old_password')
            employe = authenticate(username=email, password=old_password)
            if employe:
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')
                if new_password1 == new_password2:
                    try:
                        password_validation.validate_password(new_password1)
                    except password_validation.ValidationError as e:
                        messages.error(request, e)
                        return render(request, self.template_name, {'form': self.form, 'email': email})
                    employe = Employe.objects.get(email=email)
                    employe.set_password(new_password1)
                    employe.save()
                    login(request, employe)
                    return HttpResponseRedirect(LOGIN_REDIRECT_URL)
                else:
                    messages.error(request, "Les deux mots de passes saisis sont différents")
                    return render(request, self.template_name, {'form': self.form, 'email': email})
            else:
                messages.error(request, "Ancien Mot de Passe saisi est incorrect")
                return render(request, self.template_name, {'form': self.form, 'email': email})
        else:
            messages.error(request,"Formulaire Invalide")
            return HttpResponseRedirect(LOGIN_URL)



class ProfileView(TemplateView):
    template_name = 'Authentification/profile.html'

    def get(self, request, *args, **kwargs):
        employe = request.user
        if employe:
            context = {
                'name': employe.get_full_name(),
                'Matricule': employe.get_matricule(),
                'Fonction': employe.get_fonction(),
                'salaire': Salaire.objects.get(matricule_paie=employe).get_valeur_brute(),
                'cnss': employe.get_n_cnss(),
                'Departement': 'Ressources Humaines',#employe.get_departement(),
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

