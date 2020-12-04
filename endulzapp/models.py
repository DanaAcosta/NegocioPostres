from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Administrador(models.Model):
    id_administrador = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=50)
    
    def __str__(self):
        return self.usuario
    
class Usuario_administrador(models.Model):
    usuario = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre 


class Categoria(models.Model):
    id_categoria = models.CharField(max_length=50, primary_key=True)
    nombre_categoria = models.CharField(max_length=50)
      
    slug = models.SlugField(max_length=200,unique=True,blank=True)
    
    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    costo_por_porcion = models.IntegerField()
    
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    
    imagen = models.ImageField(default=None)
    slug = models.SlugField(max_length=200, db_index=True,default=None)
   
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.administrador


class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50,blank=True)
    apellido = models.CharField(max_length=50,blank=True)
    correo_electronico = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50,default=None)


class Direccion_cliente(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=50)
    barrio = models.CharField(max_length=50)
    inmueble = models.CharField(max_length=50)
    interior = models.CharField(max_length=25)
    numero = models.CharField(max_length=25)
    id_cliente = models.IntegerField(default=None)

class Carrito_de_compras(models.Model):
    id_carrito = models.IntegerField(primary_key=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_compra = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    #producto_en_carrito = models.ForeignKey(Producto_en_carrito, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
class Producto_en_carrito(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    unidades_por_producto = models.PositiveIntegerField()
    id_carrito = models.ForeignKey(Carrito_de_compras, on_delete=models.CASCADE)
    
class Repartidor(models.Model):
    id_repartidor = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=50)


class Factura(models.Model):
    num_factura = models.IntegerField(primary_key=True)
    precio_total = models.IntegerField()
    metodo_pago = models.CharField(max_length=50)
    usuario_repartidor = models.ForeignKey(Repartidor, on_delete=models.CASCADE)

class Factura_producto(models.Model):
    id_factura_producto = models.IntegerField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    pCarrito = models.ForeignKey(Producto_en_carrito, on_delete=models.CASCADE)
    
class Empleado(models.Model):
    id_empleado = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

class Inventario(models.Model):
    class Meta:
        unique_together = (('id_producto', 'numero_lote'),)
    id_producto = models.IntegerField()
    numero_lote = models.IntegerField()
    cantidad_disponible = models.IntegerField()
    usuario_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class Sub_inventario(models.Model):
    numero_lote = models.IntegerField(primary_key=True)
    fecha_produccion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)