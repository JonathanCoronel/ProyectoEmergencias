"""
    Manejo de urls para la aplicación
    administrativo
"""
from django.urls import path
# se importa las vistas de la aplicación
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('registro/<int:pk>/', views.registro, name='registro'),
    path('paciente/crear/', views.crear_paciente, name='crear_paciente'),
    path('listarPacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('registroFisico/<int:registro_id>/', views.registro_fisico, name='registro_fisico'), 
    path('paciente/<int:paciente_id>/registros/', views.registros_paciente, name='registros_paciente'),
 ]
