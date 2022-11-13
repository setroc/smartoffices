from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError

from .models import Usuario

# Create your views here.
def home(request):
  return render(request, 'index.html')

def crearJefe(request):
  if request.method == 'GET':
    return render(request,'signupJefe.html')
  else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        jefeUser = Usuario.objects.create_usuario(
          username=request.POST['username'],
          email=request.POST['correo'],
          nombre=request.POST['nombre'],
          apellidos=request.POST['apellidos'],
          jefe=True,
          password=request.POST['password1']
        )
        jefeUser.save()
        login(request, jefeUser)
        return redirect('jefeHome')
      except IntegrityError:
        return render(request,'signupJefe.html',{
          'error':'El usuario ya existe.'
        })
    return render(request,'signupJefe.html',{
      'error':'Las contraseñas no coinciden.'
    })

def crearTrabajador(request):
  if request.method == 'GET':
    return render(request,'signupTrabajador.html')
  else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        trabajadorUser = Usuario.objects.create_usuario(
          username=request.POST['username'],
          email=request.POST['correo'],
          nombre=request.POST['nombre'],
          apellidos=request.POST['apellidos'],
          password=request.POST['password1'],
        )
        trabajadorUser.save()
        return render(request, 'signupTrabajador.html', {'success': 'Trabajador creado correctamente.'});
      except IntegrityError:
        return render(request,'signupTrabajador.html',{
          'error':'El trabajador ya existe.'
        })
    return render(request,'signupTrabajador.html',{
      'error':'Las contraseñas no coinciden.'
    })