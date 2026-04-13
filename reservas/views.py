from django.shortcuts import render, get_object_or_404
from .models import Pista, Horario, Reserva
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render, get_object_or_404, redirect
from .models import Pista, Reserva
from django.contrib import messages
from django.utils import timezone


def home(request):
    pistas = Pista.objects.filter(activa=True)
    return render(request, 'reservas/home.html', {'pistas': pistas})

def pista_detalle(request, pista_id):
    pista = get_object_or_404(Pista, id=pista_id)
    fecha = request.GET.get("fecha", date.today())
    
    horarios = Horario.objects.all()
    reservas = Reserva.objects.filter(pista=pista, fecha=fecha)

    horarios_ocupados = reservas.values_list("horario_id", flat=True)

    return render(request, "reservas/pista_detalle.html", {
        "pista": pista,
        "fecha": fecha,
        "horarios": horarios,
        "horarios_ocupados": horarios_ocupados,

 })

@login_required
def crear_reserva(request, pista_id, horario_id, fecha):
    pista = get_object_or_404(Pista, id=pista_id)
    horario = get_object_or_404(Horario, id=horario_id)

    # Intentar crear la reserva
    reserva, creada = Reserva.objects.get_or_create(
        usuario=request.user,
        pista=pista,
        fecha=fecha,
        horario=horario
    )

    if not creada:
        # Ya estaba reservada → avisar
        return render(request, "reservas/error.html", {
            "mensaje": "Este horario ya está reservado."
        })

    return render(request, "reservas/reserva_ok.html", {"reserva": reserva})

def reservar_pista(request, pista_id):
    pista = get_object_or_404(Pista, id=pista_id)

    if request.method == "POST":
        fecha = request.POST.get("fecha")
        horario_id = request.POST.get("horario")
        if fecha and horario_id:
            horario = get_object_or_404(Horario, id=horario_id)
            Reserva.objects.create(
                pista=pista,
                usuario=request.user,
                fecha=fecha,
                horario=horario
            )
            messages.success(request, f"Reserva realizada para {pista.nombre} a las {horario}.")
            return redirect("home")
        else:
            messages.error(request, "Debes seleccionar una fecha y un horario.")

    # Para GET, mostramos los horarios de hoy como ejemplo
    fecha = request.GET.get("fecha") or timezone.now().date()
    horarios_disponibles = pista.get_horarios_disponibles(fecha)
    return render(request, "reservas/reservar.html", {
        "pista": pista,
        "horarios": horarios_disponibles,
        "fecha": fecha
    })
