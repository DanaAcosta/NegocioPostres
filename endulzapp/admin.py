from django.contrib import admin
from .models import Administrador,Usuario_administrador, Repartidor, Cliente, Producto, Carrito_de_compras, Producto_en_carrito, Direccion_cliente, Categoria
# Register your models here.

admin.site.register(Administrador)
admin.site.register(Usuario_administrador)

admin.site.register(Cliente)

admin.site.register(Categoria)
admin.site.register(Producto)

admin.site.register(Carrito_de_compras)
admin.site.register(Producto_en_carrito)

admin.site.register(Direccion_cliente)

admin.site.register(Repartidor)