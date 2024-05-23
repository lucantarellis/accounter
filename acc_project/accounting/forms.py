from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Movimiento, Caja, Denominacion

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['caja', 'denominacion', 'cantidad', 'tipo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].queryset = Denominacion.objects.none()

        if 'caja' in self.data:
            try:
                caja_id = int(self.data.get('caja'))
                caja = Caja.objects.get(id=caja_id)
                self.fields['denominacion'].queryset = Denominacion.objects.filter(moneda=caja.moneda)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['denominacion'].queryset = self.instance.caja.moneda.denominacion_set

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['nombre', 'moneda']

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']