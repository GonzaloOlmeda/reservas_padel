from django.contrib import admin
from .models import Pista, Bono, Reserva

@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'capacidad', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'ubicacion')


@admin.register(Bono)
class BonoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creditos', 'comprado_el', 'activo')
    search_fields = ('usuario__username',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','pista','fecha','hora_inicio','hora_fin','estado','pagado')
    list_filter = ('estado','pista','fecha')
    search_fields = ('usuario__username','pista__nombre')


# Register your models here.
