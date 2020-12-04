"""sitioPostres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from endulzapp import views as v
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.index, name='index'),
    path('register/', v.register, name="register"),
    #path('carrito/', v.carrito, name="carrito"),
    path('login/', v.login_view, name="login_view"),
    path('logout/', v.logout_view, name="logout_view"),
    
    path('registrarEmpleado/', v.registrarEmpleado, name="registrarEmpleado"),
    
    path('meterPostre/', v.upload, name="upload"),
    path('mostrarProductos/editarPostre/<int:postre_id>', v.update_postre),
    path('mostrarProductos/borrarPostre/<int:postre_id>', v.delete_postre),
    path('mostrarProductos/', v.listadoProductos, name="listadoProductos"),
    
    path('contacto/', v.contacto, name="contacto"),
    path('terminarCompra/', v.terminarCompra, name="terminarCompra"),
    path('', include("django.contrib.auth.urls")),


    path('agregarCarrito/<int:postre_id>', v.agregarAlCarrito),
    path('carrito/borrarCarrito/<int:postre_id>', v.borrarDelCarrito),
    path('carrito/', v.carrito, name="carrito"),
    
    path('categoria/<int:id_categoria>', v.organizarPorCategoria)

    #path('cart/', include('cart.urls', namespace='cart')), 
	#path('', include('sitioPostres.urls', namespace='postres')),


    #path('producto/', v.product_list, name="producto"),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)