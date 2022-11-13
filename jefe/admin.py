from django.contrib import admin
from .models import Equipo, EquipoHasTrabajador, Tarea, Reunion
# Register your models here.
admin.site.register(Equipo)
admin.site.register(EquipoHasTrabajador)
admin.site.register(Tarea)
admin.site.register(Reunion)