from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import RegistroForm, MovimientoForm, CajaForm
from .models import Caja, Movimiento, Denominacion

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

def get_denominaciones(request, caja_id):
    caja = Caja.objects.get(id=caja_id)
    denominaciones = Denominacion.objects.filter(moneda=caja.moneda).values('id', 'valor')
    return JsonResponse(list(denominaciones), safe=False)

@login_required
def index(request):
    cajas = Caja.objects.all()
    movimientos = Movimiento.objects.all()
    total_ingresos = sum(m.denominacion.valor * m.cantidad for m in movimientos if m.tipo == 'ingreso')
    total_egresos = sum(m.denominacion.valor * m.cantidad for m in movimientos if m.tipo == 'egreso')

    context = {
        'cajas': cajas,
        'movimientos': movimientos,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
    }

    return render(request, 'accounting/index.html', context)

@login_required
def nuevo_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MovimientoForm()
    return render(request, 'accounting/nuevo_movimiento.html', {'form': form})

@login_required
def nueva_caja(request):
    if request.method == 'POST':
        form = CajaForm(request.POST)
        if form.is_valid():
            caja = form.save(commit=False)
            caja.save()
            return redirect('/')
    else:
        form = CajaForm()
    return render(request, 'accounting/nueva_caja.html', {'form': form})

@login_required
def detalle_caja(request, caja_id):
    caja = Caja.objects.get(id=caja_id)
    movimientos = Movimiento.objects.filter(caja=caja)
    return render(request, 'accounting/detalle_caja.html', {'caja': caja, 'movimientos': movimientos})