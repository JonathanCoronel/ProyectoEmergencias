from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from administrativo.models import Paciente, Registro
from administrativo.forms import PacienteForm, RegistroForm

def index(request):
    registros = Registro.objects.all()

    informacion_template = {'registros': registros, 'numero_usuarios': len(registros)}
    return render(request, 'index.html',informacion_template)

def crear_paciente(request):
    if request.method == 'POST':
        formulario = PacienteForm(request.POST)
        if formulario.is_valid():
            nuevo_paciente = formulario.save()
            return redirect('registro', pk=nuevo_paciente.pk)
    else:
        formulario = PacienteForm()

    contexto = {'formulario': formulario}
    return render(request, 'crearPaciente.html', contexto)

def listar_pacientes(request):
    pacientes = Paciente.objects.all()

    informacion_template = {'pacientes': pacientes, 'numero_pacientes': len(pacientes)}
    return render(request, 'listadoPacientes.html', informacion_template)

def registro(request, pk=None):
    formulario_registro = RegistroForm(request.POST or None)
    formulario_paciente = PacienteForm(request.POST or None)

    if pk:
        try:
            paciente = Paciente.objects.get(pk=pk)
            formulario_registro.initial['paciente'] = paciente
        except Paciente.DoesNotExist:
            pass

    if request.method == 'POST':
        if formulario_registro.is_valid():
            formulario_registro.save()
            return redirect('index')
        elif formulario_paciente.is_valid():
            paciente_nuevo = formulario_paciente.save()
            formulario_registro.instance.paciente = paciente_nuevo
            formulario_registro.save()
            return redirect('index')

    contexto = {
        'formulario_registro': formulario_registro,
        'formulario_paciente': formulario_paciente,
    }
    return render(request, 'crearRegistro.html', contexto)
