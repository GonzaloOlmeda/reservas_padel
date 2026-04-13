from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class Pista(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    capacidad = models.PositiveIntegerField(default=4)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def get_horarios_disponibles(self, fecha):
        """
        Devuelve los horarios que no están reservados para la pista en la fecha dada.
        """
        from datetime import time
        todos_horarios = Horario.objects.all()  # todos los horarios definidos
        reservadas = Reserva.objects.filter(pista=self, fecha=fecha).values_list('horario', flat=True)
        return todos_horarios.exclude(id__in=reservadas)



class Bono(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bonos')
    creditos = models.PositiveIntegerField(default=0)
    comprado_el = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.creditos} créditos"


class Horario(models.Model):   # ✅ DEBE IR FUERA DE RESERVA
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}"


class Reserva(models.Model):   # ✅ SOLO UNA VEZ DEFINIDA
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    pagado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pista', 'fecha', 'horario')
        ordering = ['-fecha', 'horario']

    def clean(self):
        fecha_hora_inicio = datetime.datetime.combine(self.fecha, self.horario.hora_inicio)
        fecha_hora_inicio = timezone.make_aware(fecha_hora_inicio)

        if fecha_hora_inicio < timezone.now():
            raise ValidationError("No se puede reservar en el pasado.")

        qs = Reserva.objects.filter(pista=self.pista, fecha=self.fecha, horario=self.horario)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Esa franja horaria ya está reservada.")

    def __str__(self):
        return f"{self.usuario} reservó {self.pista} el {self.fecha} a las {self.horario}"
