from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import TrabajadorUpdateForm, EstadoAnimoForm
from usuario.models import Usuario
from jefe.models import Tarea, Reunion, EquipoHasTrabajador

from datetime import datetime
# Create your views here.
@login_required
def home(request):
  if request.method == 'GET':
    return render(request,'homeT.html')
  else:
    try:
      now = datetime.now()
      form = EstadoAnimoForm(request.POST)
      nuevoEstado = form.save(commit=False)
      nuevoEstado.usuario = request.user
      nuevoEstado.fecha = now.strftime("%d/%m/%Y %H:%M:%S")
      nuevoEstado.save()
      return render(request,'homeT.html', {'success':'Estado registrado'})
    except ValueError as e:
      print(e)
      return render(request,'homeT.html', {'error':'Error al registrar estado.'})


@login_required
def signout(request):
  logout(request)
  return redirect('trabajadorSignin')

def signin(request):
  if request.method == 'GET':
    return render(request, 'signinT.html');
  else:
    user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
    print(user)
    if user is None:
        return render(request, 'signinT.html', {"error": "El username o la contraseña son incorrectos."})
    login(request, user)
    return redirect('trabajadorHome')

# Perfil
@login_required
def editarPerfil(request):
  if request.method == 'GET':
    return render(request, 'editarPerfilT.html');
  else:
    form = TrabajadorUpdateForm(data=request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      return render(request, 'editarPerfilT.html', {'success': 'Datos actualizados correctamente.'});
    else:
      return render(request, 'editarPerfilT.html', {'error':'Los datos ingresados no son válidos.'});

# Tareas
@login_required
def tareas(request):
  tareas = Tarea.objects.filter(trabajador = request.user)
  return render(request, 'tareasT.html', {'tareas':tareas})

@login_required
def marcarTareaCompletada(request, tarea_id):
  if request.method == 'POST':
    try:
      tarea = get_object_or_404(Tarea, pk=tarea_id)
      tarea.completado = True
      tarea.save()
      return redirect('trabajadorTareas')
    except ValueError:
      return redirect('trabajadorTareas')

# Reuniones
@login_required
def reuniones(request):
  equipo = EquipoHasTrabajador.objects.filter(trabajador = request.user)
  for e in equipo:
    reuniones = Reunion.objects.filter(equipo = e.equipo)
    return render(request, 'reunionesT.html', {'reuniones':reuniones})
  # print(reuniones)
@login_required
def reunionRetroalimentacion(request, reunion_id):
  reunion = get_object_or_404(Reunion, pk=reunion_id)
  return render(request, 'verRetroalimentacion.html', {'reunion':reunion})
