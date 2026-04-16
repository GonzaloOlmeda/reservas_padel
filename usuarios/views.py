from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .forms import RegistroForm, LoginForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Enviar email de bienvenida
            try:
                send_mail(
                    subject='¡Bienvenido a Padel Reservas!',
                    message=f'''Hola {user.username},

¡Bienvenido a Padel Reservas!

Tu cuenta ha sido creada exitosamente. Ya puedes empezar a reservar pistas de padel comprando un bono de créditos.

Para comenzar:
1. Ve a tu perfil y compra un bono de créditos
2. Explora las pistas disponibles
3. Haz tu primera reserva

¡Esperamos verte pronto en las pistas!

Atentamente,
El equipo de Padel Reservas
''',
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log the error but don't break the registration process
                print(f"Error sending email: {e}")

            messages.success(request, f'¡Bienvenido, {user.username}! Cuenta creada correctamente.')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('login')


@login_required
def perfil(request):
    bonos = request.user.bonos.filter(activo=True)
    reservas = request.user.reservas.order_by('-fecha')[:10]

    # Calcular total de créditos disponibles
    from django.db.models import Sum
    total_creditos = bonos.aggregate(total=Sum('creditos'))['total'] or 0
    return render(request, 'usuarios/perfil.html', {
        'bonos': bonos,
        'reservas': reservas,
        'total_creditos': total_creditos,
    })