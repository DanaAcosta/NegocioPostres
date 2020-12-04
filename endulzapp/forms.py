from django import forms

from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

  
from .models import Producto, Producto_en_carrito

class FormularioRegistro(UserCreationForm):
    first_name = forms.CharField(label="nombre", max_length=100)
    last_name = forms.CharField(label="apellido", max_length=100)
    email = forms.EmailField(label="correo electronico", max_length=100)
    telefono = forms.CharField(label="telefono", max_length=10)

    direccion = forms.CharField(label="direccion", max_length=100)
    barrio = forms.CharField(label="barrio", max_length=100)
    interior = forms.CharField(label="interior", max_length=100)
    numero = forms.CharField(label="numero", max_length=100)
    inmueble = forms.CharField(label="inmueble", max_length=100)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "telefono", "direccion", "barrio", "interior", "numero", "inmueble", "email" ,"username", "password1", "password2"]

class FormularioInicioSesion(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('El usuario no existe')
            if not user.check_password(password):
                raise forms.ValidationError('Contraseña incorrecta')
            if not user.is_active:
                raise forms.ValidationError('El usuario no esta activo')
        return super(FormularioInicioSesion, self).clean(*args, **kwargs)


class CrearPostrecito(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["id_producto", "nombre", "id_categoria", "costo_por_porcion", "administrador","slug", "imagen", "descripcion"]
        
PRODUCT_unidades_por_producto_CHOICES = [(i, str(i)) for i in range(1, 21)]

class AgregarPostreAlCarrito(forms.ModelForm):
    class Meta:
        model = Producto_en_carrito
        fields = ["unidades_por_producto"]

class FormularioAddproducto(forms.Form):
	unidades_por_producto = forms.TypedChoiceField(choices=PRODUCT_unidades_por_producto_CHOICES, coerce=int)
	override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)




class FormularioRegistroEmpleado(UserCreationForm):
    first_name = forms.CharField(label="nombre", max_length=100)
    last_name = forms.CharField(label="apellido", max_length=100)
    cargo = forms.CharField(label="cargo", max_length=10)
    


    class Meta:
        model = User
        fields = ["first_name", "last_name", "cargo","username", "password1", "password2"]

