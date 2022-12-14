from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EstadoAnimo

class TrabajadorUpdateForm(forms.ModelForm):
  correo = forms.EmailField()
  nombre = forms.CharField()
  apellidos = forms.CharField()

  class Meta:
    model = User
    fields = ['username','nombre','correo','apellidos']
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].help_text = None

class EstadoAnimoForm(forms.ModelForm):
  class Meta:
    model = EstadoAnimo
    fields = ['sentimiento','texto']