from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("pista/<int:pista_id>/", views.pista_detalle, name="pista_detalle"),
    path("reservar/<int:pista_id>/<int:horario_id>/<str:fecha>/",
         views.crear_reserva, name="crear_reserva"),
    path('pista/<int:pista_id>/', views.pista_detalle, name='pista_detalle'),
    path('pista/<int:pista_id>/reservar/', views.reservar_pista, name='reservar_pista'),
]
