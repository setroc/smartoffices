from django.db import models

from usuario.models import Usuario
# Create your models here.
class EstadoAnimo(models.Model):
  usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  sentimiento = models.TextField(max_length=20)
  texto = models.TextField(max_length=1000)
  fecha = models.TextField(max_length=50)
  def __str__(self):
    return self.sentimiento + ' - ' + self.usuario.username

