from django import forms

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class FormularioRegistro(UserCreationForm):
    nombre = forms.CharField(label="nombre", max_length=100)
    apellido = forms.CharField(label="apellido", max_length=100)
    telefono = forms.CharField(label="telefono", max_length=10)
    correo = forms.EmailField(label="correo", max_length=100)

    class Meta:
        model = User
        fields = ["nombre", "apellido", "telefono", "correo", "username", "password1", "password2"]


class  CrearNuevoUsuario(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=100)
    apellido = forms.CharField(label="apellido", max_length=100)
    telefono = forms.CharField(label="telefono", max_length=10)
    correo = forms.CharField(label="correo", max_length=100)
    usuario = forms.CharField(label="usuario", max_length=100)
    contrasena = forms.CharField(label="contrasena", max_length=100)
