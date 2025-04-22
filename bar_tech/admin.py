from django.contrib import admin
from .models import *

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'telefono', 'abonos', 'restante', 'deben']

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'telefono', 'correo', 'clave', 'documento']

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['rol', 'salario', 'usuario']
    list_filter = ['rol'] 
    search_fields = ['usuario__nombre']

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('horas_inicio', 'horas_fin', 'usuario')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'categoria', 'stock', 'foto']

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'estado', 'total', 'cliente']

@admin.register(DetalleCarrito)
class DetalleCarritoAdmin(admin.ModelAdmin):
    list_display = ['precio', 'cantidad', 'mesa', 'producto', 'carrito']

