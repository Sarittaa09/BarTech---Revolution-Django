from django.db import models
from datetime import timedelta
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator, EmailValidator
from decimal import Decimal
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone

solo_letras_numeros = RegexValidator(
    regex=r'^[a-zA-Z0-9 ]+$',
    message="No se permiten caracteres especiales. Solo letras, números y espacios."
)

class Producto(models.Model):
    nombre = models.CharField(max_length=100, validators=[solo_letras_numeros])
    precio = models.IntegerField(validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    
    tipo_producto = (
        ('1', "Cervezas"),
        ('2', "Aguardiente"),
        ('3', "Gaseosas"),
        ('4', "Alta"),
        ('5', "Ron"),
        ('6', "Otros"),
    )
    categoria = models.CharField(max_length=1, choices=tipo_producto, default="1")
    foto = models.ImageField(upload_to="productos/")

    def clean(self):
        # Validación para asegurar que el stock y el precio sean mayores que 0
        if self.stock < 1:
            raise ValidationError("El stock debe ser mayor que 0.")
        if self.precio < 0:
            raise ValidationError("El precio no puede ser negativo.")

    def __str__(self):
        return f'{self.nombre}'

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, validators=[solo_letras_numeros])
    apellidos = models.CharField(max_length=100, validators=[solo_letras_numeros])
    telefono = models.CharField(max_length=15, validators=[solo_letras_numeros])
    deben = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    abonos = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    restante = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def clean(self):
        # Validación para asegurar que el teléfono tenga un formato válido (opcional)
        if len(self.telefono) < 10:
            raise ValidationError("El número de teléfono debe tener al menos 10 dígitos.")
        if self.deben < 0 or self.abonos < 0 or self.restante < 0:
            raise ValidationError("Los valores de deuda, abono o restante no pueden ser negativos.")

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'
    

class Carrito(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', message="Solo se permiten letras y espacios.")])
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def clean(self):
        if self.total < Decimal('0.00'):
            raise ValidationError("El total del carrito no puede ser negativo.")

    def __str__(self):
        return f"Carrito de {self.cliente.nombre} - Estado: {self.estado}"


class DetalleCarrito(models.Model):
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])  # La cantidad no puede ser menor que 1
    mesa = models.IntegerField(validators=[MinValueValidator(1)])  # La mesa debe ser un número positivo
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)

    def clean(self):
        if self.precio < Decimal('0.00'):
            raise ValidationError("El precio no puede ser negativo.")
        if self.cantidad < 1:
            raise ValidationError("La cantidad debe ser al menos 1.")
        if self.mesa < 1:
            raise ValidationError("El número de mesa debe ser un valor positivo.")

    def __str__(self):
        return f"Detalle del carrito {self.carrito.id} - Producto: {self.producto.nombre}"

class Usuario(models.Model):
    nombre = models.CharField(max_length=100, validators=[RegexValidator(regex=r'^[a-zA-Z ]+$', message="Solo se permiten letras y espacios.")])
    apellidos = models.CharField(max_length=100, validators=[RegexValidator(regex=r'^[a-zA-Z ]+$', message="Solo se permiten letras y espacios.")])
    telefono = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="El número de teléfono debe ser válido.")])
    correo = models.EmailField(unique=True, validators=[EmailValidator(message="Correo electrónico inválido.")])
    clave = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^[a-zA-Z0-9@#$%^&+=]*$', message="La clave solo puede contener letras, números y caracteres especiales.")])
    documento = models.CharField(max_length=20, unique=True, validators=[RegexValidator(regex=r'^\d{5,20}$', message="El documento debe ser un número válido.")])

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Cargo(models.Model):
    ROLES = (
        ('Empleado', 'Empleado'),
        ('Administrador', 'Administrador'),
    )

    rol = models.CharField(max_length=50, choices=ROLES, default='Empleado')
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def clean(self):
        if self.salario < Decimal('0.00'):
            raise ValidationError("El salario no puede ser negativo.")

    def __str__(self):
        return f"{self.rol} - {self.usuario.nombre}"

class Horario(models.Model):
    horas_inicio = models.TimeField()
    horas_fin = models.TimeField()
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    @property
    def horas_trabajadas(self):
        inicio = datetime.combine(self.fecha, self.horas_inicio)
        fin = datetime.combine(self.fecha, self.horas_fin)
        if fin < inicio:
            fin += timedelta(days=1)  # Si el fin es antes que el inicio, es al día siguiente
        total_horas = (fin - inicio).seconds / 3600
        return round(total_horas, 2)

    def clean(self):
        if self.horas_inicio >= self.horas_fin:
            raise ValidationError("La hora de inicio debe ser antes de la hora de fin.")

    def __str__(self):
        return f"Horario de {self.usuario.nombre} - Fecha: {self.fecha}"

