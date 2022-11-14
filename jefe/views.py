from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import JefeUpdateForm, EquipoForm, TrabajadorForm, AsignarEquipoForm, TareaForm, ReunionForm
from .models import Equipo, EquipoHasTrabajador, Tarea, Reunion
from usuario import models as usuarioModels
from trabajador.models import EstadoAnimo

# Create your views here.
@login_required
def home(request):
  return render(request,'home.html')

@login_required
def signout(request):
  logout(request)
  return redirect('jefeSignin')

def signin(request):
  if request.method == 'GET':
    return render(request, 'signin.html');
  else:
    user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
    if user is None:
        return render(request, 'signin.html', {"error": "El username o la contraseña son incorrectos."})
    login(request, user)
    return redirect('jefeHome')

# Perfil
@login_required
def editarPerfil(request):
  if request.method == 'GET':
    return render(request, 'editarPerfil.html');
  else:
    form = JefeUpdateForm(data=request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      return render(request, 'editarPerfil.html', {'success': 'Datos actualizados correctamente.'});
    else:
      return render(request, 'editarPerfil.html', {'error':'Los datos ingresados no son válidos.'});

# Equipo
@login_required
def crearEquipo(request):
  if request.method == "GET":
    return render(request, 'equipo/crearEquipo.html');
  else:
    try:
      form = EquipoForm(request.POST)
      new_equipo = form.save(commit=False)
      new_equipo.jefe = request.user
      new_equipo.save()
      return render(request, 'equipo/crearEquipo.html', {"success": "Equipo creado correctamente."}) 
    except ValueError:
      return render(request, 'equipo/crearEquipo.html', {"error": "Error creando equipo."}) 

@login_required
def listarEquipos(request):
  equipos = Equipo.objects.filter(jefe=request.user)
  return render(request, 'equipo/equipos.html', {"equipos": equipos})

@login_required
def editarEquipo(request, equipo_id):
  if request.method == 'GET':
    equipo = get_object_or_404(Equipo, pk=equipo_id, jefe=request.user)
    form = EquipoForm(instance=equipo)
    return render(request, 'equipo/editarEquipo.html', {'equipo': equipo})
  else:
    try:
      equipo = get_object_or_404(Equipo, pk=equipo_id, jefe=request.user)
      form = EquipoForm(data=request.POST, instance=equipo)
      if form.is_valid():
        form.save()
        return render(request, 'equipo/editarEquipo.html', {"success": "Equipo editado correctamente.",'equipo': equipo}) 
      else:
        return render(request, 'equipo/editarEquipo.html', {"error": "No se pudo editar el equipo.",'equipo': equipo}) 
    except ValueError:
      return render(request, 'equipo/editarEquipo.html', {"error": "No se pudo editar el equipo.",'equipo': equipo}) 

@login_required
def eliminarEquipo(request, equipo_id):
  equipo = get_object_or_404(Equipo, pk=equipo_id, jefe=request.user)
  if request.method == 'POST':
    equipo.delete()
    return redirect('jefeListarEquipos')

@login_required
def verEquipo(request, equipo_id):
  equipo = get_object_or_404(Equipo, pk=equipo_id, jefe=request.user)
  equipos = EquipoHasTrabajador.objects.select_related().filter(equipo=equipo_id)
  return render(request, 'equipo/equipo.html', {"equipos": equipos, 'equipo':equipo})

# Trabajadores
@login_required
def listarTrabajadores(request):
  trabajadores = usuarioModels.Usuario.objects.filter(jefe=False);
  return render(request, 'trabajador/trabajadores.html', {"trabajadores": trabajadores})

@login_required
def editarTrabajador(request, trabajador_id):
  if request.method == 'GET':
    trabajador = get_object_or_404(usuarioModels.Usuario, pk=trabajador_id)
    return render(request, 'trabajador/editarTrabajador.html', {'trabajador': trabajador})
  else:
    try:
      trabajador = get_object_or_404(usuarioModels.Usuario, pk=trabajador_id)
      form = TrabajadorForm(data=request.POST, instance=trabajador)
      if form.is_valid():
        form.save()
        return render(request, 'trabajador/editarTrabajador.html', {"success": "Trabajador editado correctamente.",'trabajador': trabajador}) 
      else:
        return render(request, 'trabajador/editarTrabajador.html', {"error": "No se pudo editar el trabajador.",'trabajador': trabajador}) 
    except ValueError:
      return render(request, 'trabajador/editarTrabajador.html', {"error": "No se pudo editar el trabajador.",'trabajador': trabajador}) 

@login_required
def eliminarTrabajador(request, trabajador_id):
  trabajador = get_object_or_404(usuarioModels.Usuario, pk=trabajador_id)
  if request.method == 'POST':
    trabajador.delete()
    return redirect('listarTrabajadores')

@login_required
def estadosTrabajador(request, trabajador_id):
  trabajador = get_object_or_404(usuarioModels.Usuario, pk=trabajador_id)
  estados = EstadoAnimo.objects.filter(usuario=trabajador)
  return render(request, 'trabajador/estadosAnimo.html',{'trabajador':trabajador,'estados':estados})

@login_required
def asignarAEquipo(request):
  if request.method == 'GET':
    equipos = Equipo.objects.filter(jefe=request.user)
    trabajadores = usuarioModels.Usuario.objects.filter(jefe=False);
    return render(request,'equipo/asignarAEquipo.html', {'equipos':equipos, 'trabajadores':trabajadores})
  else:
    try:
      equipos = Equipo.objects.filter(jefe=request.user)
      trabajadores = usuarioModels.Usuario.objects.filter(jefe=False);
      form = AsignarEquipoForm(request.POST)
      new_equipo = form.save(commit=False)
      new_equipo.save()
      return render(request,'equipo/asignarAEquipo.html', {'equipos':equipos, 'trabajadores':trabajadores, 'success':'Se agrego el trabajador al equipo correctamente.'})
    except ValueError:
      return render(request,'equipo/asignarAEquipo.html', {'equipos':equipos, 'trabajadores':trabajadores, 'error':'No se pudo agregar el trabajador al equipo.'})

# Tareas
@login_required
def asignarTareaAEquipo(request):
  equipos = Equipo.objects.filter(jefe=request.user)
  return render(request, 'tarea/asignarTarea.html', {"equipos": equipos})
@login_required
def crearTarea(request, equipo_id):
  if request.method == "GET":
    trabajadores = EquipoHasTrabajador.objects.select_related().filter(equipo=equipo_id)
    return render(request, 'tarea/crearTarea.html',{'trabajadores':trabajadores, 'equipo_id':equipo_id});
  else:
    try:
      trabajadores = EquipoHasTrabajador.objects.select_related().filter(equipo=equipo_id)
      form = TareaForm(request.POST)
      nuevaTarea = form.save(commit=False)
      nuevaTarea.equipo = get_object_or_404(Equipo, pk=equipo_id)
      nuevaTarea.save()
      return render(request, 'tarea/crearTarea.html',{'trabajadores':trabajadores, 'equipo_id':equipo_id, 'success':'Tarea asignada correctamente.'});
    except ValueError as e:
      print(e)
      return render(request, 'tarea/crearTarea.html',{'trabajadores':trabajadores, 'equipo_id':equipo_id, 'error':'Error al asignar tarea.'});
@login_required
def verTareas(request, equipo_id):
  tareas = Tarea.objects.select_related().filter(equipo=equipo_id)
  return render(request, 'tarea/tareas.html', {"tareas": tareas})

# Reunion
@login_required
def asignarReunionAEquipo(request):
  equipos = Equipo.objects.filter(jefe=request.user)
  return render(request, 'reunion/asignarReunion.html', {"equipos": equipos})

@login_required
def crearReunion(request, equipo_id):
  if request.method == "GET":
    return render(request, 'reunion/crearReunion.html',{'equipo_id':equipo_id});
  else:
    try: 
      form = ReunionForm(request.POST)
      nuevaReunion = form.save(commit=False)
      nuevaReunion.equipo = get_object_or_404(Equipo, pk=equipo_id)
      nuevaReunion.retroalimentacion = ""
      nuevaReunion.save()
      return render(request, 'reunion/crearReunion.html',{'equipo_id':equipo_id, 'success': 'Reunión creada correctamente.'})
    except ValueError as e:
        print(e)
        return render(request, 'reunion/crearReunion.html',{'equipo_id':equipo_id, 'error': 'Error al crear una reunión.'})

@login_required
def verReuniones(request, equipo_id):
  reuniones = Reunion.objects.select_related().filter(equipo=equipo_id)
  return render(request, 'reunion/reuniones.html', {"reuniones": reuniones, "equipo_id":equipo_id})

@login_required
def agregarRetroalimentacion(request,equipo_id,reunion_id):
  if request.method == "GET":
    return render(request, 'reunion/agregarRetroalimentacion.html',{'equipo_id':equipo_id,'reunion_id':reunion_id})
  else:
    try:
      reunion = get_object_or_404(Reunion, pk=reunion_id)
      reunion.retroalimentacion = request.POST['retroalimentacion']
      reunion.save()
      return redirect('jefeAsignarReunionAEquipo')
    except ValueError:
      return render(request, 'reunion/agregarRetroalimentacion.html',{'equipo_id':equipo_id,'reunion_id':reunion_id, 'error': 'Error al agregar retroalimentación.'})
