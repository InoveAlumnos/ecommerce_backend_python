#!/usr/bin/env python

from tkinter import E
from applications.ecommerce.groups import ClientGroup
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey


class BaseView(TemplateView):
    '''
    Base template
    '''
    template_name = 'ecommerce/base.html'


class LoginUserView(TemplateView):
    '''
    Formulario de inicio de sesión.
    '''
    template_name = 'ecommerce/login.html'


class UserForm(UserCreationForm):
    '''
    Formulario de creación de usuario.
    '''

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')


def register(request):
    '''
    Registro de usuario.
    
    Redireccionamientos:
        - información inválida: /signup
        - registro exitoso: /login
    '''

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            # Guardar el formulario si este es válido
            form.save()

            ClientGroup().agregar_usuario_username(request.POST.get("username"))
            # Redirigin a página de inicio de sesión
            return redirect('/ecommerce/login')

        else:
            errors = ""
            for e in form.errors.keys():
                errors += f"{form.errors[e][0]}\n"

            return render(request, 'ecommerce/signup.html', {'form': form, 'errors': errors})

    else:

        # Crear un objeto de tipo formulario y enviarlo al contexto de renderización
        form = UserForm()
    
    return render(request, 'ecommerce/signup.html', dict(form = form))


class IndexView(TemplateView):
    '''
    Página principal del sitio.
    '''

    template_name = 'ecommerce/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Borrar api-keys viejas en caso de que existan
        try:
            APIKey.objects.filter(name = self.request.user.username).delete()
        except:
            pass

        if self.request.user.is_authenticated:
            context["api_key"] = APIKey.objects.create_key(name = self.request.user.username)[1]

        return context


class TutorialView(TemplateView):
    '''
    Página de tutorial.
    '''

    template_name = 'ecommerce/tutorial.html'