from django.shortcuts import render, redirect, get_object_or_404
from .utilidades import verify_password
from .models import *
from django.contrib import messages
from .forms import ProductoForm, HorarioForm, FiltroHorarioForm
from django.utils import timezone


# Create your views here.

def index(request):
    verificar = request.session.get("path", False)
    
    if verificar:
        return render(request, "index.html")
    else:
        return redirect('primera')

def login(request):
    verificar = request.session.get("path", False)
    if verificar:
        return redirect("index")
    else:
        if request.method == "POST":
            correo = request.POST.get("correo")
            clave = request.POST.get("clave")
            try:
                q = Usuario.objects.get(correo=correo, clave=clave)
                # print(q)
                #if verify_password(clave, q.clave):
                request.session["path"] = {
                    "id": q.id,
                    "nombre": q.nombre,
                    "apellido": q.apellidos,
                    "correo": q.correo,
                    "telefono": q.telefono,
                }
                return redirect("index")
                # else:
                #     raise Usuario.DoesNotExist()
                
            except Usuario.DoesNotExist:
                print("Usuario o contraseña incorrectos")
                messages.warning(request, "Usuario o contraseña incorrectos")
                request.session["path"] = None
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, f"Error: {e}")
                request.session["path"] = None
            return redirect("login")
        else:
            verificar = request.session.get("path", False)
            if verificar:
                return redirect("index")
            else:
                return render(request, "login.html")

def logout(request):
    verificar = request.session.get("path", False)
    if verificar:
        del request.session["path"]
        return redirect("primera")
    else:
        return redirect("login")

def crear_cuenta_cliente(request):
    if request.method == "POST":
        nombre = request.POST.get('nombreCliente')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        total_fiado = request.POST.get('totalFiado')

        Cliente.objects.create(
                nombre=nombre,
                apellidos=apellidos,  
                telefono=telefono,  
                deben=total_fiado
            )
        return redirect('fiados1')  

    return render(request, 'crear_cuenta.html')


def vista_aguardiente(request):
    aguardiente = Producto.objects.filter(categoria=2)
    return render(request, 'aguardiente.html', {'aguardiente': aguardiente})

def vista_alta(request):
    alta = Producto.objects.filter(categoria=4)
    return render(request, 'alta.html', {'alta': alta})

def vista_cerveza(request):
    cerveza = Producto.objects.filter(categoria=1)
    return render(request, 'cervezas.html', {'cerveza': cerveza})

def vista_g(request):
    g = Producto.objects.filter(categoria=3)
    return render(request, 'g.html', {'lista_g': g})

def vista_otro(request):
    otro = Producto.objects.filter(categoria=6)
    return render(request, 'otro.html', {'otro': otro})

def primera(request):
    return render(request, 'primera.html')

def vista_rones(request):
    rones = Producto.objects.filter(categoria=5)
    return render(request, 'rones.html', {'rones': rones})

def ventas_del_dia(request):
    ventas = DetalleCarrito.objects.all()  # Obtén todas las ventas
    return render(request, "carrito.html", {"ventas": ventas})

def lista_fiados(request):
    nombre_filtro = request.GET.get('nombre', '')
    if nombre_filtro:
        clientes = Cliente.objects.filter(nombre__icontains=nombre_filtro)
    else:
        clientes = Cliente.objects.all()

    datos_clientes = [{'cliente': cliente} for cliente in clientes]
    
    return render(request, 'fiados1.html', {
        'datos_clientes': datos_clientes
    })

def fiados2(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    ventas = Venta.objects.filter(cliente=cliente)

    if request.method == 'POST':
        abonos = request.POST.get('abono')
        if abonos:
            abonos = float(abonos)
            
            venta = ventas.first()
            if venta:
                venta.abonos += abonos
                venta.restante -= abonos
                venta.save()

                
                cliente.deben -= abonos
                cliente.save()

        return redirect('fiados2', cliente_id=cliente.id)

    return render(request, 'fiados2.html', {
        'cliente': cliente,
        'ventas': ventas
    })

def registrar_abono(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        abono = request.POST.get('abono')

        if cliente_id and abono:
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                abono_decimal = Decimal(abono)
                
                cliente.abonos += float(abono_decimal)
                cliente.restante -= float(abono_decimal)
                cliente.deben -= abono_decimal

                # Asegura que no sea negativo
                if cliente.restante < 0:
                    cliente.restante = 0
                if cliente.deben < 0:
                    cliente.deben = 0

                cliente.save()
            except Cliente.DoesNotExist:
                pass  # Cliente no válido
            except Exception as e:
                print("Error al registrar abono:", e)

    return redirect('lista_fiados')

def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreCliente')
        apellido = request.POST.get('apellidoCliente')
        telefono = request.POST.get('telefonoCliente')
        categoria = request.POST.get('categoriaCliente')
        total_fiado = request.POST.get('totalFiado')

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            categoria=categoria,
            deben=total_fiado
        )
        return redirect('fiados1')  # A donde quieras redirigir
    return render(request, 'crear_cuenta.html')


def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('fiados1')

def nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto registrado correctamente.')
            return redirect('nuevo_producto')  # o a donde quieras redirigir
    else:
        form = ProductoForm()
    
    productos = Producto.objects.all()
    return render(request, 'nuevo_producto.html', {'form': form, 'productos': productos})

def registro_horarios(request):
    horarios = Horario.objects.all().order_by('-fecha')
    form = HorarioForm()
    filtro_form = FiltroHorarioForm(request.GET or None)

    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_horarios')

    if filtro_form.is_valid():
        if filtro_form.cleaned_data.get('fecha'):
            horarios = horarios.filter(fecha=filtro_form.cleaned_data['fecha'])
        if filtro_form.cleaned_data.get('trabajador'):
            horarios = horarios.filter(usuario=filtro_form.cleaned_data['trabajador'])

    return render(request, 'horarios.html', {
        'form': form,
        'filtro_form': filtro_form,
        'horarios': horarios
    })

def eliminar_horario(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)
    horario.delete()
    return redirect('registro_horarios')

def agregar_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))

        producto = Producto.objects.get(id=producto_id)

        # Aquí puedes usar sesión o un modelo temporal (ej: Carrito por usuario)
        carrito = request.session.get('carrito', [])
        carrito.append({'id': producto.id, 'nombre': producto.nombre, 'cantidad': cantidad, 'precio': float(producto.precio)})
        request.session['carrito'] = carrito
        messages.success(request, f"Producto '{producto.nombre}' añadido correctamente al carrito.")

        return redirect('ver_carrito')
    return redirect('ver_carrito')

# Ver carrito
def ver_carrito(request):
    carrito = request.session.get('carrito', [])
    total_items = []

    for item in carrito:
        producto = Producto.objects.get(id=item['id'])  # Convertir a objeto real
        total = item['cantidad'] * item['precio']
        total_items.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'total': total
        })

    clientes = Cliente.objects.all()
    usuarios = Usuario.objects.all()

    return render(request, 'carrito.html', {
        'carrito': total_items,
        'clientes': clientes,
        'usuarios': usuarios
    })


# Finalizar venta
def finalizar_venta(request):
    if request.method == 'POST':
        # guardar la venta aquí usando los datos del carrito y del formulario
        request.session['carrito'] = [] 
        messages.success(request, "¡Pedido finalizado correctamente!")
        return redirect('index')
    
def editar_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        nueva_cantidad = int(request.POST.get('cantidad', 1))

        carrito = request.session.get('carrito', [])
        for item in carrito:
            if str(item['id']) == str(producto_id):
                item['cantidad'] = nueva_cantidad
                break
        request.session['carrito'] = carrito
    return redirect('ver_carrito')


# Eliminar producto
def eliminar_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')

        carrito = request.session.get('carrito', [])
        carrito = [item for item in carrito if str(item['id']) != str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('ver_carrito')