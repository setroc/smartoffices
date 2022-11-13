from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.conf import settings

# Create your models here.
class UsuarioManager(BaseUserManager):
  def create_usuario(self, username, email, nombre, apellidos, password = None, jefe = False ):
    if not email:
      raise ValueError('El usuario debe tener un correo')
    usuario = self.model(
      username = username,
      email = self.normalize_email(email),
      nombre = nombre,
      apellidos = apellidos,
      jefe = jefe
    )
    usuario.set_password(password)
    usuario.save()
    return usuario
  def create_superuser(self, username, email, nombre, apellidos, password):
    usuario = self.create_usuario(username, email, nombre, apellidos, password)
    usuario.administrador = True
    usuario.save()
    return usuario

class Usuario(AbstractBaseUser):
  username = models.CharField('Username',unique=True, max_length=100)
  email = models.EmailField('Correo electrónico',unique=True, max_length=100)
  nombre = models.CharField('Nombre', max_length=100, blank=False)
  apellidos = models.CharField('Apellidos', max_length=200, blank=False)
  administrador = models.BooleanField(default=False)
  jefe = models.BooleanField(default=False)
  objects = UsuarioManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email','nombre','apellidos']

  def __str__(self):
    return f'Usuario {self.username}'
  def has_perm(self,perm,obj=None):
    return True
  def has_module_perms(self,app_label):
    return True
  
  @property
  def is_staff(self):
    return self.administrador