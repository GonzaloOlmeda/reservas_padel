from django.contrib import admin
from .models import Pista, Bono, Horario, Reserva


@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion", "capacidad", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre", "ubicacion")


@admin.register(Bono)
class BonoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "creditos", "comprado_el", "activo")
    list_filter = ("activo",)
    search_fields = ("usuario__username",)


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("hora_inicio", "hora_fin")
    ordering = ("hora_inicio",)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "pista", "fecha", "get_hora_inicio", "get_hora_fin", "estado", "pagado")
    list_filter = ("fecha", "estado", "pista")
    search_fields = ("usuario__username", "pista__nombre")

    # métodos para mostrar las horas en el admin
    def get_hora_inicio(self, obj):
        return obj.horario.hora_inicio
    get_hora_inicio.short_description = "Hora inicio"

    def get_hora_fin(self, obj):
        return obj.horario.hora_fin
    get_hora_fin.short_description = "Hora fin"
