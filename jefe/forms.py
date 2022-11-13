from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Equipo, EquipoHasTrabajador, Tarea
from usuario import models as UsuarioModel

class JefeCreationForm(UserCreationForm):
  correo = forms.EmailField()
  nombre = forms.CharField()
  apellidos = forms.CharField()

  class Meta:
    model = User
    fields = ['username','nombre','correo','apellidos','password1','password2']
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].help_text = None
    self.fields['password1'].help_text = None
    self.fields['password2'].help_text = None

class JefeUpdateForm(forms.ModelForm):
  correo = forms.EmailField()
  nombre = forms.CharField()
  apellidos = forms.CharField()

  class Meta:
    model = User
    fields = ['username','nombre','correo','apellidos']
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].help_text = None

class EquipoForm(forms.ModelForm):
  class Meta:
    model = Equipo
    fields = ['titulo', 'descripcion']

class TrabajadorForm(forms.ModelForm):
  class Meta:
    model = UsuarioModel.Usuario
    fields = ['username','email','nombre','apellidos']

class AsignarEquipoForm(forms.ModelForm):
  class Meta:
    model = EquipoHasTrabajador
    fields = ['equipo','trabajador']

class TareaForm(forms.ModelForm):
  class Meta:
    model = Tarea
    fields = ['trabajador','titulo','descripcion']