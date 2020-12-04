from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .forms import FormularioRegistro, FormularioInicioSesion, CrearPostrecito, AgregarPostreAlCarrito, FormularioRegistroEmpleado
from .models import Cliente, User, Direccion_cliente, Producto, Producto_en_carrito, Carrito_de_compras, Empleado, Administrador, Factura, Factura_producto, Repartidor, Direccion_cliente
from django.contrib.auth import authenticate,get_user_model,login,logout

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import FormularioAddproducto

import datetime

# Create your views here.

def index(request):
    shelf = Producto.objects.all()

    carrito = AgregarPostreAlCarrito()
    carrito.fields['unidades_por_producto'].initial = 0
    if request.method == 'POST':
        carrito = AgregarPostreAlCarrito(request.POST, request.FILES)
        if carrito.is_valid():
            carrito.save()
            return redirect('/')
        else:

            return HttpResponse('Los datos a cargar son inválidos.')
    else:
        return render(request,'index.html', {'shelf': shelf,'carrito': carrito})
    
    
    


def register(response):
    if response.method == "POST":
        registro = FormularioRegistro(response.POST)
            
        if registro.is_valid():
            telefono = registro.cleaned_data["telefono"]
            correo = registro.cleaned_data["email"]
            nombre = registro.cleaned_data["first_name"]
            apellido = registro.cleaned_data["last_name"]

            direccion = registro.cleaned_data["direccion"]
            barrio = registro.cleaned_data["barrio"]
            interior = registro.cleaned_data["interior"]
            numero = registro.cleaned_data["numero"]
            inmueble = registro.cleaned_data["inmueble"]
            
            registro.save()
            
            ultimoId = User.objects.latest('id').id

            
            cliente = Cliente(id_cliente=ultimoId,correo_electronico=correo,telefono=telefono, nombre=nombre, apellido=apellido)
            cliente.save()

            ultimoIdDireccion = 1
            try:
                ultimoIdDireccion = Direccion_cliente.objects.latest('id_direccion').id_direccion+1
            except: 
                ultimoIdDireccion = 1

            direccion = Direccion_cliente(id_direccion=ultimoIdDireccion, barrio=barrio, direccion=direccion,inmueble=inmueble,interior=interior,numero=numero,id_cliente=ultimoId)           
            direccion.save()
            
            return redirect('/login')
        else:
            return redirect('/')
            
    else:
        registro = FormularioRegistro()
        
        x = registro.fields['username']
        x.label = "Usuario"
        
        x = registro.fields['password1']
        x.label = "Contraseña"
        
        x = registro.fields['password2']
        x.label = "Confirmar contraseña"
        
    return render(response, "endulzapp/register.html", {"form":registro})

def login_view(request):
    next = request.GET.get('next')
    form = FormularioInicioSesion(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)

        return redirect('/')
    
    return render(request, "endulzapp/login.html", {"form":form})

def logout_view(request):
    logout(request)
    return redirect('/')


#@login_required
def carrito(request):
    if request.user.is_authenticated:
        usuario_actual = request.user
        
        carritoCliente = Carrito_de_compras.objects.filter(cliente=usuario_actual.id, fecha_compra=datetime.date.today(), fecha_entrega=None)
        
        try:
            postresEnCarrito = Producto_en_carrito.objects.filter(id_carrito=carritoCliente[0])
        except:
            postresEnCarrito = []
             
        listaDeProuctosYCantidades = []

        totalCuenta = 0
        for querys in postresEnCarrito:
            productosEnCarrito = Producto.objects.get(id_producto=querys.id_producto.id_producto)
            listaDeProuctosYCantidades.append([productosEnCarrito,querys.unidades_por_producto])
            
            totalCuenta += listaDeProuctosYCantidades[-1][0].costo_por_porcion*listaDeProuctosYCantidades[-1][1]


        return render(request, "endulzapp/carrito.html", {"postresEnCarrito":listaDeProuctosYCantidades, "totalCuenta":totalCuenta})
    else:
        return redirect('/login')


def borrarDelCarrito(request, postre_id):
    if request.user.is_authenticated:
        usuario_actual = request.user
        carritoCliente = Carrito_de_compras.objects.filter(cliente=usuario_actual.id, fecha_compra=datetime.date.today())
    
        borrarProducto = Producto_en_carrito.objects.get(id_carrito=carritoCliente[0], id_producto=postre_id)
        borrarProducto.delete()
        
        return redirect('/carrito')
    else:
        return redirect('/login')
    
#@login_required
def upload(request):
    if request.user.is_authenticated and request.user.is_superuser:
        upload = CrearPostrecito()
        if request.method == 'POST':
            upload = CrearPostrecito(request.POST, request.FILES)
            if upload.is_valid():
                upload.save()
                return redirect('/')
            else:
                return HttpResponse('Los datos a cargar son inválidos.')
        else:
            return render(request, 'endulzapp/subirPostre.html', {'upload_form': upload})
    
    else:
        return redirect('/login')



def update_postre(request, postre_id):
    if request.user.is_authenticated and request.user.is_superuser:
        postre_id = int(postre_id)
        
        try:
            postre_seleccionado = Producto.objects.get(id_producto=postre_id)
        except Producto.DoesNotExist:
            return redirect('/')
        
        formulario_postre = CrearPostrecito(request.POST or None, instance=postre_seleccionado)
        
        if formulario_postre.is_valid():
            formulario_postre.save()
            return redirect('/')
        
        return render(request, 'endulzapp/subirPostre.html', {'upload_form': formulario_postre})
    
    else:
        return redirect('/login')

def delete_postre(request, postre_id):
    postre_id = int(postre_id)
    try:
        postre_seleccionado = Producto.objects.get(id_producto=postre_id)
    except Producto.DoesNotExist:
        return redirect('/mostrarProductos')
    postre_seleccionado.delete()
    return redirect('/mostrarProductos/') 


def listadoProductos(request):
    shelf = Producto.objects.all()
    return render(request, 'endulzapp/mostrarProductos.html', {'shelf': shelf})


def agregarAlCarrito(request, postre_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            carrito = AgregarPostreAlCarrito(request.POST, request.FILES)
            if carrito.is_valid():
                usuario_actual = request.user
                
                clienteYaTieneCarrito = Carrito_de_compras.objects.filter(cliente=usuario_actual.id)
                                
                global idCarritoCliente
                yaComproHoy = False
                if len(clienteYaTieneCarrito) == 0:   
                    try:
                        idCarritoCliente = Carrito_de_compras.objects.latest('id_carrito').id_carrito+1
                    except: 
                        idCarritoCliente = 1
                
                else:
                    for tuplasDelCliente in clienteYaTieneCarrito:
                        if tuplasDelCliente.fecha_compra == datetime.date.today() and tuplasDelCliente.fecha_entrega == None:
                            yaComproHoy = True
                            break
                        else:
                            yaComproHoy = False
                            
      
                    if yaComproHoy:
                        idCarritoCliente = Carrito_de_compras.objects.latest('id_carrito').id_carrito
                    else:
                        idCarritoCliente = Carrito_de_compras.objects.latest('id_carrito').id_carrito+1
                        
                agregarCarrito = Carrito_de_compras(id_carrito=idCarritoCliente,fecha_compra=datetime.date.today(), cliente=Cliente.objects.get(id_cliente=usuario_actual.id))
                agregarCarrito.save()
                
                agregarAlCarrito = Producto_en_carrito(id_carrito=Carrito_de_compras.objects.get(id_carrito=idCarritoCliente), unidades_por_producto=carrito.cleaned_data.get("unidades_por_producto"), id_producto=Producto.objects.get(id_producto=postre_id))
                agregarAlCarrito.save()
                
                return redirect('/')
            else:

                return HttpResponse('Los datos a cargar son inválidos.')
        else:
            return render(request, '/', {'carrito': carrito})
    
    else:
        return redirect('/login')
    

def registrarEmpleado(response):
    if response.user.is_authenticated and response.user.is_superuser:
        if response.method == "POST":
            registro = FormularioRegistro(response.POST)
  
            if registro.is_valid():
                nombre = registro.cleaned_data["first_name"]
                apellido = registro.cleaned_data["last_name"]
                cargo = registro.cleaned_data["cargo"]
           
                registro.save()
                
                ultimoId = User.objects.latest('id').id

                
                ultimoIdEmpleado = 1
                try:
                    ultimoIdEmpleado = Empleado.objects.latest('id_empleado').id_empleado+1
                except: 
                    ultimoIdEmpleado = 1
                    
                empleado = Empleado(administrador=Administrador.objects.get(id_administrador=ultimoId), nombre=nombre, apellido=apellido, id_empleado=ultimoIdEmpleado, cargo=cargo)
                empleado.save()
                    
                    
        else:
            registro = FormularioRegistroEmpleado()
            
            x = registro.fields['username']
            x.label = "Usuario"
            
            x = registro.fields['password1']
            x.label = "Contraseña"
            
            x = registro.fields['password2']
            x.label = "Confirmar contraseña"

            return render(response, "endulzapp/register.html", {"form":registro})
    else:
        return redirect('/login')
    

def organizarPorCategoria(request, id_categoria):
    shelf = Producto.objects.filter(id_categoria=id_categoria)
    
    carrito = AgregarPostreAlCarrito()
    carrito.fields['unidades_por_producto'].initial = 0
    if request.method == 'POST':
        carrito = AgregarPostreAlCarrito(request.POST, request.FILES)
        if carrito.is_valid():
            carrito.save()
            return redirect('/categoria/'+id_categoria)
        else:

            return HttpResponse('Los datos a cargar son inválidos.')

    return render(request,'endulzapp/filtrarPorCategoria.html', {'shelf': shelf,'carrito': carrito})

def contacto(request):
    return render(request,'endulzapp/contacto.html', {})

def terminarCompra(request):
    if request.user.is_authenticated:
        usuario_actual = request.user
        
        carritoCliente = Carrito_de_compras.objects.filter(cliente=usuario_actual.id, fecha_compra=datetime.date.today(), fecha_entrega=None)
        
        try:
            postresEnCarrito = Producto_en_carrito.objects.filter(id_carrito=carritoCliente[0])
        except:
            postresEnCarrito = []
             
        listaDeProuctosYCantidades = []

        totalCuenta = 0
        for querys in postresEnCarrito:
            productosEnCarrito = Producto.objects.get(id_producto=querys.id_producto.id_producto)
            listaDeProuctosYCantidades.append([productosEnCarrito,querys.unidades_por_producto])
            
            totalCuenta += listaDeProuctosYCantidades[-1][0].costo_por_porcion*listaDeProuctosYCantidades[-1][1]

        ultimoNumeroFactura = 1
        try:
            ultimoNumeroFactura = Factura.objects.latest('num_factura').num_factura + 1
        except:
            ultimoNumeroFactura = 1
            
        factura = Factura(num_factura=ultimoNumeroFactura, precio_total=totalCuenta,metodo_pago="Efectivo",usuario_repartidor=Repartidor.objects.get(id_repartidor=1))
        factura.save()
        
        ultimoNumeroProductoFacturaProducto = 1
        try:
            ultimoNumeroProductoFacturaProducto = Factura_producto.objects.latest('id_factura_producto').id_factura_producto + 1
        except:
            ultimoNumeroProductoFacturaProducto = 1
            
        
            
        for productos in postresEnCarrito:   
            factura_producto = Factura_producto(id_factura_producto=ultimoNumeroProductoFacturaProducto,factura=Factura.objects.get(num_factura=ultimoNumeroFactura),pCarrito=productos)
            factura_producto.save()
            
            ultimoNumeroProductoFacturaProducto += 1
            
        
        direccion = Direccion_cliente.objects.get(id_cliente=usuario_actual.id)
        
        domiciliario = Repartidor.objects.get(id_repartidor=1)
        domiciliario = domiciliario.nombre + " " + domiciliario.apellido
        
        cerrarCarrito = Carrito_de_compras.objects.get(cliente=usuario_actual.id, fecha_compra=datetime.date.today(), fecha_entrega=None)
        cerrarCarrito.fecha_entrega = datetime.date.today()
        cerrarCarrito.save()
        
        return render(request,'endulzapp/confirmarCompra.html', {"postresEnCarrito":listaDeProuctosYCantidades, "totalCuenta":totalCuenta, "numFactura":ultimoNumeroFactura, "direccion":direccion, "domiciliario":domiciliario})
    else:
        return redirect('/login')
    
    
    
    
    