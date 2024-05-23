from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('nuevo_movimiento/', views.nuevo_movimiento, name='nuevo_movimiento'),
    path('nueva_caja/', views.nueva_caja, name='nueva_caja'),
    path('detalle_caja/<int:caja_id>/', views.detalle_caja, name='detalle_caja'),
    path('get_denominaciones/<int:caja_id>/', views.get_denominaciones, name='get_denominaciones'),
]