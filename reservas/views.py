from django.shortcuts import render, get_object_or_404, redirect
from .models import Pista, Horario, Reserva, Bono
from datetime import date, datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django import forms
from django.core.mail import send_mail


class ComprarBonoForm(forms.Form):
    PAQUETES_CHOICES = [
        (5, '5 créditos - €5'),
        (10, '10 créditos - €10'),
        (20, '20 créditos - €20'),
    ]
    paquete = forms.ChoiceField(choices=PAQUETES_CHOICES, widget=forms.RadioSelect)


def consumir_credito(usuario):
    """
    Consume 1 crédito del bono más antiguo activo del usuario.
    Retorna True si se consumió correctamente, False si no hay créditos.
    """
    bono = Bono.objects.filter(
        usuario=usuario,
        activo=True,
        creditos__gt=0
    ).order_by('comprado_el').first()

    if bono:
        bono.creditos -= 1
        if bono.creditos == 0:
            bono.activo = False
        bono.save()
        return True
    return False


def get_creditos_restantes(usuario):
    """
    Retorna el total de créditos disponibles del usuario.
    """
    from django.db.models import Sum
    return Bono.objects.filter(
        usuario=usuario,
        activo=True
    ).aggregate(total=Sum('creditos'))['total'] or 0


def home(request):
    pistas = Pista.objects.filter(activa=True)
    return render(request, 'reservas/home.html', {'pistas': pistas})

@login_required(login_url='login')
def pista_detalle(request, pista_id):
    pista = get_object_or_404(Pista, id=pista_id)
    fecha_param = request.GET.get("fecha")
    try:
        fecha = date.fromisoformat(fecha_param) if fecha_param else date.today()
    except ValueError:
        fecha = date.today()

    horarios = Horario.objects.all().order_by('hora_inicio')
    reservas = Reserva.objects.filter(pista=pista, fecha=fecha)

    horarios_ocupados = reservas.values_list("horario_id", flat=True)

    return render(request, "reservas/pista_detalle.html", {
        "pista": pista,
        "fecha": fecha,
        "horarios": horarios,
        "horarios_ocupados": horarios_ocupados,
    })

@login_required(login_url='login')
def crear_reserva(request, pista_id, horario_id, fecha):
    pista = get_object_or_404(Pista, id=pista_id)
    horario = get_object_or_404(Horario, id=horario_id)

    # Verificar si el usuario tiene créditos disponibles
    if not consumir_credito(request.user):
        messages.error(request, 'No tienes créditos suficientes. Compra un bono para reservar.')
        return redirect('comprar_bono')

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

    # Enviar email de confirmación
    creditos_restantes = get_creditos_restantes(request.user)
    try:
        send_mail(
            subject='Confirmación de reserva - Padel Reservas',
            message=f'''Hola {request.user.username},

Tu reserva ha sido confirmada exitosamente:

🏓 Pista: {pista.nombre}
📅 Fecha: {fecha}
⏰ Horario: {horario}
💰 Créditos restantes: {creditos_restantes}

¡Gracias por usar Padel Reservas!

Atentamente,
El equipo de Padel Reservas
''',
            from_email=None,
            recipient_list=[request.user.email],
            fail_silently=True,
        )
    except Exception as e:
        # Log the error but don't break the reservation process
        print(f"Error sending email: {e}")

    return render(request, "reservas/reserva_ok.html", {"reserva": reserva})

@login_required(login_url='login')
def reservar_pista(request, pista_id):
    pista = get_object_or_404(Pista, id=pista_id)

    if request.method == "POST":
        fecha = request.POST.get("fecha")
        horario_id = request.POST.get("horario")
        if fecha and horario_id:
            horario = get_object_or_404(Horario, id=horario_id)

            # Verificar si el usuario tiene créditos disponibles
            if not consumir_credito(request.user):
                messages.error(request, 'No tienes créditos suficientes. Compra un bono para reservar.')
                return redirect('comprar_bono')

            Reserva.objects.create(
                pista=pista,
                usuario=request.user,
                fecha=fecha,
                horario=horario
            )

            # Enviar email de confirmación
            creditos_restantes = get_creditos_restantes(request.user)
            try:
                send_mail(
                    subject='Confirmación de reserva - Padel Reservas',
                    message=f'''Hola {request.user.username},

Tu reserva ha sido confirmada exitosamente:

🏓 Pista: {pista.nombre}
📅 Fecha: {fecha}
⏰ Horario: {horario}
💰 Créditos restantes: {creditos_restantes}

¡Gracias por usar Padel Reservas!

Atentamente,
El equipo de Padel Reservas
''',
                    from_email=None,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log the error but don't break the reservation process
                print(f"Error sending email: {e}")

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


@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha', '-horario__hora_inicio')
    ahora = timezone.localtime()

    for reserva in reservas:
        fecha_hora_inicio = datetime.combine(reserva.fecha, reserva.horario.hora_inicio)
        fecha_hora_inicio = timezone.make_aware(fecha_hora_inicio, timezone.get_current_timezone())
        reserva.puede_cancelar = fecha_hora_inicio > ahora and reserva.estado != 'cancelada'

    return render(request, 'reservas/mis_reservas.html', {
        'reservas': reservas,
    })


@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'rol') and request.user.rol == 'admin')):
        return redirect('home')

    User = get_user_model()
    total_pistas = Pista.objects.count()
    total_horarios = Horario.objects.count()
    total_reservas = Reserva.objects.count()
    reservas_confirmadas = Reserva.objects.filter(estado='confirmada').count()
    reservas_canceladas = Reserva.objects.filter(estado='cancelada').count()
    total_bonos = Bono.objects.count()
    total_usuarios = User.objects.filter(rol='cliente').count()
    total_admins = User.objects.filter(rol='admin').count()

    return render(request, 'reservas/admin_dashboard.html', {
        'total_pistas': total_pistas,
        'total_horarios': total_horarios,
        'total_reservas': total_reservas,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_canceladas': reservas_canceladas,
        'total_bonos': total_bonos,
        'total_usuarios': total_usuarios,
        'total_admins': total_admins,
    })


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id, usuario=request.user)
    fecha_hora_inicio = datetime.combine(reserva.fecha, reserva.horario.hora_inicio)
    fecha_hora_inicio = timezone.make_aware(fecha_hora_inicio, timezone.get_current_timezone())

    if reserva.estado == 'cancelada':
        messages.warning(request, 'Esta reserva ya estaba cancelada.')
        return redirect('mis_reservas')

    if fecha_hora_inicio <= timezone.localtime():
        messages.error(request, 'No puedes cancelar una reserva que ya ha pasado.')
        return redirect('mis_reservas')

    reserva.estado = 'cancelada'
    reserva.save()

    # Enviar email de cancelación
    creditos_restantes = get_creditos_restantes(request.user)
    try:
        send_mail(
            subject='Cancelación de reserva - Padel Reservas',
            message=f'''Hola {request.user.username},

Tu reserva ha sido cancelada exitosamente:

🏓 Pista: {reserva.pista.nombre}
📅 Fecha: {reserva.fecha}
⏰ Horario: {reserva.horario}
💰 Créditos restantes: {creditos_restantes}

Si necesitas hacer una nueva reserva, puedes hacerlo desde nuestra plataforma.

Atentamente,
El equipo de Padel Reservas
''',
            from_email=None,
            recipient_list=[request.user.email],
            fail_silently=True,
        )
    except Exception as e:
        # Log the error but don't break the cancellation process
        print(f"Error sending email: {e}")

    messages.success(request, 'Reserva cancelada correctamente.')
    return redirect('mis_reservas')


@login_required
def comprar_bono(request):
    if request.method == 'POST':
        form = ComprarBonoForm(request.POST)
        if form.is_valid():
            creditos = int(form.cleaned_data['paquete'])
            Bono.objects.create(
                usuario=request.user,
                creditos=creditos,
                activo=True
            )

            # Enviar email de confirmación de compra
            creditos_restantes = get_creditos_restantes(request.user)
            try:
                send_mail(
                    subject='Confirmación de compra de bono - Padel Reservas',
                    message=f'''Hola {request.user.username},

¡Tu bono ha sido comprado exitosamente!

💰 Créditos comprados: {creditos}
💰 Créditos totales disponibles: {creditos_restantes}

Ya puedes empezar a reservar pistas de padel.

¡Gracias por elegir Padel Reservas!

Atentamente,
El equipo de Padel Reservas
''',
                    from_email=None,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log the error but don't break the purchase process
                print(f"Error sending email: {e}")

            messages.success(request, f'¡Bono de {creditos} créditos comprado correctamente!')
            return redirect('perfil')
    else:
        form = ComprarBonoForm()

    return render(request, 'reservas/comprar_bono.html', {'form': form})
