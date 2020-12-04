from decimal import Decimal 
from django.conf import settings
from endulzapp.models import Producto
from endulzapp.models import Producto_en_carrito


class Cart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

def add(self, producto):
	if str(producto.id_producto) not in self.cart.keys():
		self.cart[product.id] = {
			"producto_id" : producto.id_producto,
			"nombre" : producto.nombre,
			"cantidad": 1,
			"precio": str(producto.costo_por_unidad),
			"imagen": producto.image.url
		}
	else:
		for key, value in self.cart.items():
			if key == str(producto.id_producto):
				value["cantidad"] = value["cantidad"]+1
				self.save()
				break
	self.save

def save(self):
	self.session[settings.CART_SESSION_ID]=self.cart
	self.session.modified=True

def remove(self, producto):
	producto_id = str(producto.id_producto)
	if producto_id in self.cart:
		del self.cart[producto_id]
		self.save()

def decrement(self, producto):
	for key, value in self.cart.items():
		if key == str(producto.id_producto):
			value["cantidad"] = value["cantidad"]-1
			if value["cantidad"] < 1:
				self.remove(producto)
			else:
				self.save()
			break
		else:
			print("El producto no existe en el carrito")

def __iter__(self):
	"""Iterate over the items in the cart and get the products from the database."""
	id_ps = self.cart.keys()
	# get the product objects and add them to the cart
	productos = Producto.objects.filter(id__in=id_ps)
	cart = self.cart.copy()
	for producto in productos:
		cart[str(Producto_en_carrito.id_producto)]['producto'] = producto
	for item in cart.values():
		item['costo_por_porcion'] = Decimal(item['costo_por_porcion'])
		item['total_costo_por_porcion'] = item['costo_por_porcion'] * item['unidades_por_producto']
		yield item

def __len__(self):
    """Count all items in the cart."""
    return sum(item['unidades_por_producto'] for item in self.cart.values())

def get_total_costo_por_porcion(self):
    return sum(Decimal(item['costo_por_porcion']) * item['unidades_por_producto'] for item in self.cart.values())

def clear(self):
    # remove cart from session
	del self.session[settings.CART_SESSION_ID]
	self.save()
