from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.conf import settings


from usuario import models as usuarioModels

# Create your models here.

class Equipo(models.Model):
  titulo = models.CharField(max_length=200)
  descripcion = models.TextField(max_length=1000)
  jefe = models.ForeignKey(usuarioModels.Usuario, on_delete=models.CASCADE)

  def __str__(self):
    return self.titulo + ' - ' + self.jefe.username

class EquipoHasTrabajador(models.Model):
  equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
  trabajador = models.OneToOneField(usuarioModels.Usuario, on_delete=models.CASCADE)
  def __str__(self):
    return self.equipo.titulo + ' - ' + self.trabajador.username

class Tarea(models.Model):
  equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
  trabajador = models.ForeignKey(usuarioModels.Usuario, on_delete=models.CASCADE)
  titulo = models.CharField(max_length=200)
  descripcion = models.TextField(max_length=1000)
  completado = models.BooleanField(default=False)
  def __str__(self):
    return self.equipo.titulo + ' - ' + self.titulo

class Reunion(models.Model):
  equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
  titulo = models.CharField(max_length=200)
  link = models.CharField(max_length=200)
  descripcion = models.TextField(max_length=1000)
  fecha = models.CharField(max_length=50)
  retroalimentacion = models.TextField(max_length=1000, default="")
  def __str__(self):
    return self.equipo.titulo + ' - ' + self.titulo