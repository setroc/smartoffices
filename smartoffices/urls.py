"""smartoffices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jefe import views as jefeViews
from trabajador import views as trabajador
from usuario import views as usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    # usuario inicio
    path('',usuario.home, name='home'),
    # Jefe
    path('jefe/', jefeViews.home, name='jefeHome'),
    path('user/signupJefe/',usuario.crearJefe, name='signupJefe' ),
    path('jefe/signin/', jefeViews.signin, name='jefeSignin'),
    path('jefe/signout/', jefeViews.signout, name='jefeSignout'),
    path('jefe/edit/', jefeViews.editarPerfil, name='jefeEditarPerfil'),
    # Jefe - Equipos
    path('jefe/newTeam/', jefeViews.crearEquipo, name='jefeCrearEquipo'),
    path('jefe/teams/', jefeViews.listarEquipos, name='jefeListarEquipos'),
    path('jefe/teams/<int:equipo_id>', jefeViews.editarEquipo, name='jefeEditarEquipo'),
    path('jefe/teams/<int:equipo_id>/ver', jefeViews.verEquipo, name='jefeVerEquipo'),
    path('jefe/teams/<int:equipo_id>/delete', jefeViews.eliminarEquipo, name='jefeEliminarEquipo'),
    path('jefe/teams/asignar/', jefeViews.asignarAEquipo, name='jefeAsignarAEquipo'),
    
    path('jefe/teams/tarea/', jefeViews.asignarTareaAEquipo, name='jefeAsignarTareaAEquipo'),
    path('jefe/teams/tarea/<int:equipo_id>', jefeViews.crearTarea, name='jefeCrearTarea'),
    path('jefe/teams/tarea/<int:equipo_id>/ver', jefeViews.verTareas, name='jefeVerTareas'),

    path('jefe/teams/reunion/', jefeViews.asignarReunionAEquipo, name='jefeAsignarReunionAEquipo'),
    path('jefe/teams/reunion/<int:equipo_id>', jefeViews.crearReunion, name='jefeCrearReunion'),
    path('jefe/teams/reunion/<int:equipo_id>/ver', jefeViews.verReuniones, name='jefeVerReuniones'),
    # Jefe - Trabajadores
    path('user/signupTrabajador/',usuario.crearTrabajador, name='signupTrabajador' ),
    path('jefe/trabajadores/',jefeViews.listarTrabajadores, name='listarTrabajadores' ),
    path('jefe/trabajadores/<int:trabajador_id>', jefeViews.editarTrabajador, name='editarTrabajador'),
    path('jefe/trabajadores/<int:trabajador_id>/delete', jefeViews.eliminarTrabajador, name='eliminarTrabajador'),

    # Trabajador
    path('trabajador/', trabajador.home, name='trabajadorHome'),
    path('trabajador/signin/', trabajador.signin, name='trabajadorSignin'),
    path('trabajador/signout/', trabajador.signout, name='trabajadorSignout'),
    path('trabajador/edit/', trabajador.editarPerfil, name='trabajadorEditarPerfil'),

    # Trabajador tareas
    path('trabajador/tareas', trabajador.tareas, name='trabajadorTareas'),

    # Trabajador reuniones
    path('trabajador/reuniones', trabajador.reuniones, name='trabajadorReuniones'),
]
