from django.contrib import admin
from .models import Administrador,Usuario_administrador, Cliente,Usuario_cliente
# Register your models here.

admin.site.register(Administrador)
admin.site.register(Usuario_administrador)

admin.site.register(Cliente)
admin.site.register(Usuario_cliente)