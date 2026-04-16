from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('bonos/comprar/', views.comprar_bono, name='comprar_bono'),
    path('pista/<int:pista_id>/reservar/', views.reservar_pista, name='reservar_pista'),
    path('pista/<int:pista_id>/', views.pista_detalle, name='pista_detalle'),
    path('reservar/<int:pista_id>/<int:horario_id>/<str:fecha>/',
         views.crear_reserva, name='crear_reserva'),
]
