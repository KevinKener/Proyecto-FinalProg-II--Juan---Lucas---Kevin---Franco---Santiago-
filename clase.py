from datetime import date
from typing import List

# Clase Producto
class Producto:
    def __init__(self, id: int, nombre: str, descripcion: str, precio: float, plataforma: str, imagen: str):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.plataforma = plataforma
        self.imagen = imagen

    def mostrar_detalles(self):
        # Implementación de la función mostrar detalles
        pass

    def aplicar_descuento(self, descuento: float):
        # Implementación de la función aplicar descuento
        pass

# Clase Usuario
class Usuario:
    def __init__(self, id: int, nombre_usuario: str, correo_electronico: str, contrasena: str):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena

    def iniciar_sesion(self):
        # Implementación de la función iniciar sesión
        pass

    def cerrar_sesion(self):
        # Implementación de la función cerrar sesión
        pass

# Clase ItemCarrito
class ItemCarrito:
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad

# Clase Carrito
class Carrito:
    def __init__(self, id: int, usuario: Usuario):
        self.id = id
        self.usuario = usuario
        self.items: List[ItemCarrito] = []

    def agregar_producto(self, producto: Producto, cantidad: int):
        # Implementación de la función agregar producto
        item = ItemCarrito(producto, cantidad)
        self.items.append(item)

    def eliminar_producto(self, id_producto: int):
        
        self.items = [item for item in self.items if item.producto.id != id_producto]

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.items)

# Clase Pago
class Pago:
    def __init__(self, id: int, tipo: str, monto: float):
        self.id = id
        self.tipo = tipo
        self.monto = monto

    def procesar_pago(self):
        
        pass

# Clase Orden
class Orden:
    def __init__(self, id: int, usuario: Usuario, items: List[ItemCarrito], fecha: date, total: float):
        self.id = id
        self.usuario = usuario
        self.items = items
        self.fecha = fecha
        self.total = total

    def generar_orden(self):
        
        pass

    def calcular_total(self):
        
        pass

# Clase Contacto
class Contacto:
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    def enviar_mensaje(self):
        
        pass
