from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CrearNuevoUsuario, FormularioRegistro
from .models import Cliente,Usuario_cliente

# Create your views here.

def register(response):
    if response.method == "POST":
        registro = FormularioRegistro(response.POST)
        
        if registro.is_valid():
            print("El registro es invalido")
            nombre = registro.cleaned_data["nombre"]
            apellido = registro.cleaned_data["apellido"]
            correo = registro.cleaned_data["correo"]
            telefono = registro.cleaned_data["telefono"]
            usuario = registro.cleaned_data["username"]
            contrasena = registro.cleaned_data["password1"]           

            clienteAnterior = Cliente.objects.values_list("id_cliente")
            ultimoId = 0
            for c in clienteAnterior:
                ultimoId = c[0]

            cliente = Cliente(id_cliente=ultimoId+1,correo_electronico=correo)
           
            usuario_cliente = Usuario_cliente(usuario=usuario,nombre=nombre,apellido=apellido,
                                              contrasena=contrasena,correo_electronico=correo,
                                              telefono=telefono,cliente=cliente)
            cliente.save()
            usuario_cliente.save()     

        return redirect("/admin")
    else:
        registro = FormularioRegistro()
    return render(response, "endulzapp/register.html", {"form":registro})

""" def register(response):
    if response.method == "POST":
        registro = CrearNuevoUsuario(response.POST)
        if registro.is_valid():
            nombre = registro.cleaned_data["nombre"]
            apellido = registro.cleaned_data["apellido"]
            correo = registro.cleaned_data["correo"]
            telefono = registro.cleaned_data["telefono"]
            usuario = registro.cleaned_data["usuario"]
            contrasena = registro.cleaned_data["contrasena"]

            clienteAnterior = Cliente.objects.values_list("id_cliente")

            ultimoId = 0
            for c in clienteAnterior:
                ultimoId = c[0]
            print("EL ID Que LE TOCA A ESA CHIMBADA ES: ", ultimoId+1)

            cliente = Cliente(id_cliente=ultimoId+1,correo_electronico=correo)
           
            usuario_cliente = Usuario_cliente(usuario=usuario,nombre=nombre,apellido=apellido,
                                              contrasena=contrasena,correo_electronico=correo,
                                              telefono=telefono,cliente=cliente)
            cliente.save()
            usuario_cliente.save()

        return HttpResponseRedirect("/admin")
    else:        
        form = CrearNuevoUsuario()

    return render(response, "endulzapp/register.html",{"form":form}) """