from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm
)
from django.forms.fields import (
    CharField, BooleanField
)
from django.forms.widgets import (
    PasswordInput, CheckboxInput
)
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .functions import (
    validate_email, validate_username
    )
from .models import *

from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    """!
    Clase del formulario de logeo

    @date 01-03-2017
    @version 1.0.0
    """
    ## Campo de la constraseña
    contrasena = CharField()

    ## Nombre del usuario
    usuario = CharField()

    ## Formulario de recordarme
    remember_me = BooleanField()

    ## Campo del captcha
    #captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['contrasena'].widget = PasswordInput()
        self.fields['contrasena'].widget.attrs.update({'placeholder': 'Contraseña'})
        self.fields['usuario'].widget.attrs.update({'placeholder': 'Nombre de Usuario'})
        self.fields['remember_me'].label = "Recordar"
        self.fields['remember_me'].widget = CheckboxInput()
        self.fields['remember_me'].required = False
        #self.fields['captcha'].label = "Captcha"
        #self.fields['captcha'].widget.attrs.update({'class': 'validate'})

    def clean(self):
        """!
        Método que valida si el usuario a autenticar es valido

        @date 21-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con los errores
        """
        usuario = self.cleaned_data['usuario']
        contrasena = self.cleaned_data['contrasena']
        usuario = authenticate(username=usuario,password=contrasena)
        if(not usuario):
            msg = "Verifique su usuario o contraseña"
            self.add_error('usuario', msg)

    class Meta:
        fields = ('usuario', 'contrasena', 'remember_me')


class UserRegisterForm(UserCreationForm):
    """!
    Formulario de Registro

    @date 20-04-2017
    @version 1.0.0
    """
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].required = True
        self.fields['username'].label = 'Nombre de Usuario'

        self.fields['password1'].required = True
        self.fields['password1'].label = 'Constraseña'

        self.fields['password2'].required = True
        self.fields['password2'].label = 'Repita su constraseña'

        self.fields['first_name'].label = 'Nombre'

        self.fields['last_name'].label = 'Apellido'

        self.fields['email'].label = 'Correo'

    def clean_password_repeat(self):
        """!
        Método que valida si las contraseñas coinciden

        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        password = self.cleaned_data['password1']
        password_repeat = self.cleaned_data['password2']
        if(password_repeat!=password):
            raise forms.ValidationError("La contraseña no coincide")
        return password_repeat

    def clean_email(self):
        """!
        Método que valida si el correo es única

        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        email = self.cleaned_data['email']
        if(validate_email(email)):
            raise forms.ValidationError("El correo ingresado ya existe")
        return email


class PasswordResetForm(PasswordResetForm):
    """!
    Clase del formulario de resetear contraseña

    @date 02-05-2017
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Correo'})

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email = cleaned_data.get("email")

        if email:
            msg = "Error no existe el email"
            try:
                User.objects.get(email=email)
            except:
                self.add_error('email', msg)



class PasswordConfirmForm(SetPasswordForm):
    """!
    Formulario para confirmar la constraseña

    @date 15-05-2017
    @version 1.0.0
    """
    def __init__(self, *args, **kwargs):
        super(PasswordConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Contraseña Nueva'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Repita su Contraseña'})


class PasswordChangeForms(forms.Form):
    """!
    Formulario de Registro

    @date 20-02-2018
    @version 1.0.0
    """
    ## Antigua Contraseña
    old_password = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Antigua contraseña"
        )

    ## Nueva Contraseña
    new_password = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Nueva contraseña"
        )

    ## Repita la Nueva Contraseña
    new_password_repeat = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Repita su nueva contraseña"
        )


class PasswordChangeAccount(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeAccount, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Antigua contraseña'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Contraseña Nueva'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Repita su Contraseña'}) 

class ProfileForm(forms.ModelForm):
    
    ##  Dirección
    address = forms.CharField(widget=forms.Textarea())

    ##  Dirección
    phone = forms.CharField()

    ##  Dirección
    gender = forms.ChoiceField(widget=forms.Select(),
        choices=(('F','Femenino'),('M','Masculino')))  
    
    class Meta:
        model = Profile
        exclude = ['user']    