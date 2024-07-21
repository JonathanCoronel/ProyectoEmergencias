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

def registros_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    registros = Registro.objects.filter(paciente=paciente).order_by('-fecha_hora')

    registros_con_alertas = []
    previous = None

    for registro in registros:
        alertas = {}
        if previous:
            print("-------------------")
            if registro.frecuencia_cardiaca < previous.frecuencia_cardiaca:
                alertas['frecuencia_cardiaca'] = 'Frecuencia Cardiaca Aumentando'
            elif registro.frecuencia_cardiaca > previous.frecuencia_cardiaca:
                alertas['frecuencia_cardiaca'] = 'Frecuencia Cardiaca Disminuyendo'

            if registro.frecuencia_respiratoria < previous.frecuencia_respiratoria:
                alertas['frecuencia_respiratoria'] = 'Frecuencia Respiratoria Aumentando'
            elif registro.frecuencia_respiratoria > previous.frecuencia_respiratoria:
                alertas['frecuencia_respiratoria'] = 'Frecuencia Respiratoria Disminuyendo'

            if registro.presion_arterial_sistolica < previous.presion_arterial_sistolica:
                alertas['presion_arterial_sistolica'] = 'Presión Sistólica Aumentando'
            elif registro.presion_arterial_sistolica > previous.presion_arterial_sistolica:
                alertas['presion_arterial_sistolica'] = 'Presión Sistólica Disminuyendo'

            if registro.presion_arterial_diastolica < previous.presion_arterial_diastolica:
                alertas['presion_arterial_diastolica'] = 'Presión Diastólica Aumentando'
            elif registro.presion_arterial_diastolica > previous.presion_arterial_diastolica:
                alertas['presion_arterial_diastolica'] = 'Presión Diastólica Disminuyendo'

            if registro.saturacion_oxigeno < previous.saturacion_oxigeno:
                alertas['saturacion_oxigeno'] = 'Saturación de Oxígeno Aumentando'
            elif registro.saturacion_oxigeno > previous.saturacion_oxigeno:
                alertas['saturacion_oxigeno'] = 'Saturación de Oxígeno Disminuyendo'

            if registro.temperatura < previous.temperatura:
                alertas['temperatura'] = 'Temperatura Aumentando'
            elif registro.temperatura > previous.temperatura:
                alertas['temperatura'] = 'Temperatura Disminuyendo'

        registros_con_alertas.append((registro, alertas))
        previous = registro

    if request.method == 'POST':
        formulario_registro = RegistroForm(request.POST)
        if formulario_registro.is_valid():
            nuevo_registro = formulario_registro.save(commit=False)
            nuevo_registro.paciente = paciente
            nuevo_registro.save()

            # Limpiar alertas anteriores
            registros_con_alertas.clear()

            # Reconstruir alertas con el nuevo registro
            registros = Registro.objects.filter(paciente=paciente).order_by('-fecha_hora')
            previous = None

            for registro in registros:
                alertas = {}
                if previous:
                    if registro.frecuencia_cardiaca < previous.frecuencia_cardiaca:
                        alertas['frecuencia_cardiaca'] = 'Frecuencia Cardiaca Aumentando'
                    elif registro.frecuencia_cardiaca > previous.frecuencia_cardiaca:
                        alertas['frecuencia_cardiaca'] = 'Frecuencia Cardiaca Disminuyendo'

                    if registro.frecuencia_respiratoria < previous.frecuencia_respiratoria:
                        alertas['frecuencia_respiratoria'] = 'Frecuencia Respiratoria Aumentando'
                    elif registro.frecuencia_respiratoria > previous.frecuencia_respiratoria:
                        alertas['frecuencia_respiratoria'] = 'Frecuencia Respiratoria Disminuyendo'

                    if registro.presion_arterial_sistolica < previous.presion_arterial_sistolica:
                        alertas['presion_arterial_sistolica'] = 'Presión Sistólica Aumentando'
                    elif registro.presion_arterial_sistolica > previous.presion_arterial_sistolica:
                        alertas['presion_arterial_sistolica'] = 'Presión Sistólica Disminuyendo'

                    if registro.presion_arterial_diastolica < previous.presion_arterial_diastolica:
                        alertas['presion_arterial_diastolica'] = 'Presión Diastólica Aumentando'
                    elif registro.presion_arterial_diastolica > previous.presion_arterial_diastolica:
                        alertas['presion_arterial_diastolica'] = 'Presión Diastólica Disminuyendo'

                    if registro.saturacion_oxigeno < previous.saturacion_oxigeno:
                        alertas['saturacion_oxigeno'] = 'Saturación de Oxígeno Aumentando'
                    elif registro.saturacion_oxigeno > previous.saturacion_oxigeno:
                        alertas['saturacion_oxigeno'] = 'Saturación de Oxígeno Disminuyendo'

                    if registro.temperatura < previous.temperatura:
                        alertas['temperatura'] = 'Temperatura Aumentando'
                    elif registro.temperatura > previous.temperatura:
                        alertas['temperatura'] = 'Temperatura Disminuyendo'

                registros_con_alertas.append((registro, alertas))
                previous = registro

    contexto = {
        'paciente': paciente,
        'registros_con_alertas': registros_con_alertas,
    }
    return render(request, 'registrosPaciente.html', contexto)
