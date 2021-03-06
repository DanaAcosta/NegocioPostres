# Generated by Django 3.1.2 on 2020-12-03 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id_administrador', models.IntegerField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Carrito_de_compras',
            fields=[
                ('id_carrito', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('fecha_compra', models.DateField(blank=True, null=True)),
                ('fecha_entrega', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('apellido', models.CharField(blank=True, max_length=50)),
                ('correo_electronico', models.CharField(max_length=50)),
                ('telefono', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion_cliente',
            fields=[
                ('id_direccion', models.AutoField(primary_key=True, serialize=False)),
                ('direccion', models.CharField(max_length=50)),
                ('barrio', models.CharField(max_length=50)),
                ('inmueble', models.CharField(max_length=50)),
                ('interior', models.CharField(max_length=25)),
                ('numero', models.CharField(max_length=25)),
                ('id_cliente', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id_empleado', models.IntegerField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=50)),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.administrador')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('num_factura', models.IntegerField(primary_key=True, serialize=False)),
                ('precio_total', models.IntegerField()),
                ('metodo_pago', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_producto', models.IntegerField()),
                ('numero_lote', models.IntegerField()),
                ('cantidad_disponible', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('costo_por_porcion', models.IntegerField()),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('imagen', models.ImageField(default=None, upload_to='')),
                ('slug', models.SlugField(default=None, max_length=200)),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.administrador')),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Repartidor',
            fields=[
                ('id_repartidor', models.IntegerField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_repartidor',
            fields=[
                ('usuario', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('contrasena', models.CharField(max_length=50)),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.administrador')),
                ('id_repartidor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.repartidor')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_empleado',
            fields=[
                ('usuario', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('cargo', models.CharField(max_length=50)),
                ('contrasena', models.CharField(max_length=50)),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.administrador')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_administrador',
            fields=[
                ('usuario', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('contrasena', models.CharField(max_length=50)),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.administrador')),
            ],
        ),
        migrations.CreateModel(
            name='Sub_inventario',
            fields=[
                ('numero_lote', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha_produccion', models.DateField(blank=True, null=True)),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Producto_en_carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades_por_producto', models.PositiveIntegerField()),
                ('id_carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.carrito_de_compras')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.producto')),
            ],
        ),
        migrations.AddField(
            model_name='inventario',
            name='usuario_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.usuario_empleado'),
        ),
        migrations.CreateModel(
            name='Factura_producto',
            fields=[
                ('id_factura_producto', models.IntegerField(primary_key=True, serialize=False)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.factura')),
                ('pCarrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.producto_en_carrito')),
            ],
        ),
        migrations.AddField(
            model_name='factura',
            name='usuario_repartidor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.usuario_repartidor'),
        ),
        migrations.AddField(
            model_name='carrito_de_compras',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endulzapp.cliente'),
        ),
        migrations.AlterUniqueTogether(
            name='inventario',
            unique_together={('id_producto', 'numero_lote')},
        ),
    ]
