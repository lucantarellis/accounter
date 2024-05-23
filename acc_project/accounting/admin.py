from django.contrib import admin

from .models import Moneda, Denominacion, Caja, Movimiento

# Register your models here.
@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo')

@admin.register(Denominacion)
class DenominacionAdmin(admin.ModelAdmin):
    list_display = ('moneda', 'valor')

@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'moneda')

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('caja', 'denominacion', 'cantidad', 'tipo', 'fecha')