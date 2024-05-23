from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Moneda(models.Model):
    nombre = models.CharField(max_length=10)
    codigo = models.CharField(max_length=3)  # ARS, USD, EUR, etc.

    def __str__(self):
        return self.nombre

class Denominacion(models.Model):
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.moneda.codigo} {self.valor}"

class Caja(models.Model):
    nombre = models.CharField(max_length=100)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)

    def total_dinero(self):
        total = 0
        for movimiento in self.movimiento_set.all():
            if movimiento.tipo == 'ingreso':
                total += movimiento.cantidad * movimiento.denominacion.valor
            elif movimiento.tipo == 'egreso':
                total -= movimiento.cantidad * movimiento.denominacion.valor
        return total
    
    def __str__(self):
        return self.nombre
    
class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
        ('Compra', 'Compra'),
        ('Venta', 'Venta'),
    ]

    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    denominacion = models.ForeignKey(Denominacion, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} - {self.cantidad} x {self.denominacion}'