from django.shortcuts import render
from .models import Pista

def home(request):
    pistas = Pista.objects.filter(activa=True)
    return render(request, 'reservas/home.html', {'pistas': pistas})


