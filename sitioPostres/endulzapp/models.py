from django.db import models

# Create your models here.

class Administrador(models.Model):
    id_administrador = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=50)

class Usuario_administrador(models.Model):
    usuario = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    costo_por_porcion = models.IntegerField()
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

class Categoria(models.Model):
    nombre_producto = models.CharField(max_length=50, primary_key=True)
    nombre_categoria = models.CharField(max_length=50)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    correo_electronico = models.CharField(max_length=50)

class Usuario_cliente(models.Model):
    correo_electronico = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre 

class Direccion_cliente(models.Model):
    id_direccion = models.IntegerField(primary_key=True)
    barrio = models.CharField(max_length=50)
    via_principal = models.CharField(max_length=50)
    numero_via_principal = models.CharField(max_length=10)
    via_auxiliar = models.CharField(max_length=50)
    numero_via_auxiliar = models.CharField(max_length=10)
    inmueble = models.CharField(max_length=50)
    interior = models.CharField(max_length=25)
    numero = models.CharField(max_length=25)

class Producto_en_carrito(models.Model):
    id_carrito = models.IntegerField(primary_key=True)
    unidades_por_producto = models.IntegerField()
    cantidad_de_productos = models.IntegerField()
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Carrito_de_compras(models.Model):
    id_carrito = models.IntegerField(primary_key=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_compra = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    producto_en_carrito = models.ForeignKey(Producto_en_carrito, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Repartidor(models.Model):
    id_repartidor = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=50)

class Usuario_repartidor(models.Model):
    usuario = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    id_repartidor = models.ForeignKey(Repartidor, on_delete=models.CASCADE)

class Factura(models.Model):
    num_factura = models.IntegerField(primary_key=True)
    precio_total = models.IntegerField()
    metodo_pago = models.CharField(max_length=50)
    usuario_repartidor = models.ForeignKey(Usuario_repartidor, on_delete=models.CASCADE)

class Empleado(models.Model):
    id_empleado = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=50)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

class Usuario_empleado(models.Model):
    usuario = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class Inventario(models.Model):
    class Meta:
        unique_together = (('id_producto', 'numero_lote'),)
    id_producto = models.IntegerField()
    numero_lote = models.IntegerField()
    cantidad_disponible = models.IntegerField()
    usuario_empleado = models.ForeignKey(Usuario_empleado, on_delete=models.CASCADE)

class Sub_inventario(models.Model):
    numero_lote = models.IntegerField(primary_key=True)
    fecha_produccion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)