import os

from django.conf import settings
from django.db import models


class Vendedor(models.Model):
    usuario = models.CharField(20)
    nombre = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)
    foto_perfil = models.FilePathField(
        path=os.path.join(settings.BASE_DIR, "app/static/"),
        default=os.path.join(settings.BASE_DIR, "app/static/dummy.png"),
    )
    OPCIONES_ACTIVIDAD = (
        ('A', 'Activo'),
        ('I', 'Inactivo')
    )
    actividad = models.CharField(
        max_length=1,
        choices=OPCIONES_ACTIVIDAD,
        default='I'
    )
    OPCIONES_FORMAS_DE_PAGO = (
        ('F00', 'Forma0'),
        ('F01', 'Forma1'),
        ('F02', 'Forma2'),
        ('F03', 'Forma3'),
    )
    formas_de_pago = models.CharField(
        max_length=3,
        choices=OPCIONES_FORMAS_DE_PAGO,
        default='F00',
    )
    latitud = models.FloatField()
    longitud = models.FloatField()

    class Meta:
        abstract = True


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
    OPCIONES_CATEGORIA = (
        ('C00', 'Categoria0'),
        ('C01', 'Categoria1'),
        ('C02', 'Categoria2'),
        ('C03', 'Categoria3'),
    )
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
    usuario = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=50)


class Seguimiento(models.Model):
    alumno = models.ForeignKey(Alumno)
    vendedor = models.ForeignKey(Vendedor)
