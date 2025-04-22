from django.urls import path
from . import views


urlpatterns = [
    path('', views.primera, name="primera"),
    path('index/', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('aguardiente/', views.vista_aguardiente, name="aguardiente"),
    path('agregar-carrito/', views.agregar_carrito, name='agregar_carrito'),
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'),
    path('finalizar-venta/', views.finalizar_venta, name='finalizar_venta'),
    path('carrito/editar/', views.editar_carrito, name='editar_carrito'),
    path('carrito/eliminar/', views.eliminar_carrito, name='eliminar_carrito'),
    path('alta/', views.vista_alta, name="alta"),
    path('cerveza/', views.vista_cerveza, name="cerveza"),
    path('g/', views.vista_g, name="g"),
    path('otro/', views.vista_otro, name="otro"),
    path('rones/', views.vista_rones, name="rones"),
    path('nuevo_producto/', views.nuevo_producto, name='nuevo_producto'),
    path('fiados/<int:cliente_id>/', views.fiados2, name='fiados2'),
    path('crear-cliente/', views.crear_cliente, name='crear_cliente'),
    path('eliminar-cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('abonar/', views.registrar_abono, name='registrar_abono'),
    path('registro-horarios/', views.registro_horarios, name='registro_horarios'),
    path('horarios/eliminar/<int:horario_id>/', views.eliminar_horario, name='eliminar_horario'),
    path("ventas-del-dia/", views.ventas_del_dia, name="ventas"),
    path('crear-cuenta/', views.crear_cuenta_cliente, name='crear_cuenta_cliente'),
    path('fiados/', views.lista_fiados, name='lista_fiados'),
    path('fiados/detalles/<int:cliente_id>/', views.fiados2, name='detalles_fiado'),
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
]

