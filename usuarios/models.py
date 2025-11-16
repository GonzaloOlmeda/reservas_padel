from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ROL_CHOICES = (
        ('usuario', 'Usuario'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='usuario')

    # Evitar conflictos con auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='usuarios_set',  # <- nombre diferente
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='grupos',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_set',  # <- nombre diferente
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario',
    )

    def es_admin(self):
        return self.rol == 'admin' or self.is_staff or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.rol})"
