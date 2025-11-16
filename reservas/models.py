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


class Bono(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bonos')
    creditos = models.PositiveIntegerField(default=0)
    comprado_el = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.creditos} créditos"


class Reserva(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    pagado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pista','fecha','hora_inicio'], name='unique_reserva_pista_fecha_horainicio')
        ]
        ordering = ['-fecha', 'hora_inicio']

    def clean(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")
        fecha_hora_inicio = datetime.datetime.combine(self.fecha, self.hora_inicio)
        fecha_hora_inicio = timezone.make_aware(fecha_hora_inicio)
        if fecha_hora_inicio < timezone.now():
            raise ValidationError("No se puede reservar en el pasado.")
        qs = Reserva.objects.filter(pista=self.pista, fecha=self.fecha, hora_inicio=self.hora_inicio)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Esa franja horaria ya está reservada.")

    def __str__(self):
        return f"Reserva #{self.id} - {self.usuario} - {self.pista} {self.fecha} {self.hora_inicio}"
