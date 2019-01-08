from django.shortcuts import render, redirect
from django.views.generic import (
    FormView, RedirectView, CreateView, 
    UpdateView, ListView, TemplateView, DeleteView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import check_password
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.http import HttpResponseForbidden, JsonResponse
from .forms import *
from .models import *



class LoginView(FormView):
    """!
    Clase que gestiona la vista principal del logeo de usuario

    @date 01-03-2017
    @version 1.0.0
    """
    form_class = LoginForm
    template_name = 'user.login.html'
    success_url = reverse_lazy('users:register')

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es valido
    
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        usuario = form.cleaned_data['usuario']
        contrasena = form.cleaned_data['contrasena']
        usuario = authenticate(username=usuario, password=contrasena)
        login(self.request, usuario)
        if self.request.POST.get('remember_me') is not None:
            # Session expira a los dos meses si no se deslogea
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)
    
    
class LogoutView(RedirectView):
    """!
    Clase que gestiona la vista principal del deslogeo de usuario

    @date 01-03-2017
    @version 1.0.0
    """
    permanent = False
    query_string = True

    def get_redirect_url(self):
        """!
        Metodo que permite definir la url de dirección al ser válido el formulario
    
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna la url
        """
        logout(self.request)
        return reverse_lazy('users:login')


class RegisterView(SuccessMessageMixin,CreateView):
    """!
    Muestra el formulario de registro de usuarios

    @date 09-01-2017
    @version 1.0.0
    """
    template_name = "user.register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:register')
    success_message = "Se registró con éxito"
    model = User


class ChangePasswordView(LoginRequiredMixin,FormView):
    """!
    Clase que gestion el cambio de contraseña

    @date 20-02-2018
    @version 1.0.0
    """
    template_name = "change_password.form.html"
    form_class = PasswordChangeAccount
    success_url = reverse_lazy('users:register')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """!
        Metodo que sobreescribe la acción por POST
    
        @date 20-02-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param pk <b>{int}</b> Recibe el id del perfil
        @return Retorna los datos de contexto
        """
        user = form.save()
        try:
            login(self.request, user)
        except:
            return super().form_valid(form)    
        return super().form_valid(form)

class ListProfileView(LoginRequiredMixin,ListView):
    template_name = "profile/profile.list.html"
    model = Profile
    paginate_by = 5

class CreateProfileView(LoginRequiredMixin,CreateView):
    template_name = "profile/profile.create.html"
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile_list')

    def form_valid(self,form):
        print(self.request.user)
        self.object = form.save(commit=False)
        self.object.address = form.cleaned_data['address']
        self.object.phone = form.cleaned_data['phone']
        self.object.gender = form.cleaned_data['gender']
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)