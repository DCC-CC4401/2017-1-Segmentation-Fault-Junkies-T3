import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

OPCIONES_ACTIVIDAD = (
    ('A', 'Activo'),
    ('I', 'Inactivo')
)

OPCIONES_FORMAS_DE_PAGO = (
    ('F00', 'Forma0'),
    ('F01', 'Forma1'),
    ('F02', 'Forma2'),
    ('F03', 'Forma3'),
)

OPCIONES_CATEGORIA = (
    ('C00', 'Categoria0'),
    ('C01', 'Categoria1'),
    ('C02', 'Categoria2'),
    ('C03', 'Categoria3'),
)

class Vendedor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foto_perfil = models.FilePathField(
        path=os.path.join(settings.BASE_DIR, "app/static/uploads/avatars"),
        default=os.path.join(settings.BASE_DIR, "app/static/dummy.png"),
    )
    actividad = models.CharField(
        max_length=1,
        choices=OPCIONES_ACTIVIDAD,
        default='I'
    )
    formas_de_pago = models.CharField(
        max_length=3,
        choices=OPCIONES_FORMAS_DE_PAGO,
        default='F00',
    )
    latitud = models.FloatField(null=True)
    longitud = models.FloatField(null=True)

    def __str__(self):
        return self.user.email


class Vendedor_Fijo(Vendedor):
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()


class Vendedor_Ambulante(Vendedor):
    pass


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    categoria = models.CharField(
        max_length=3,
        choices=OPCIONES_CATEGORIA,
        default='C00',
    )
    foto = models.ImageField()
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE
    )


class Alumno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Seguimiento(models.Model):
    alumno = models.ForeignKey(Alumno)
    vendedor = models.ForeignKey(Vendedor)
