from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cedula = models.CharField(max_length=30, unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    correo = models.EmailField()
    telefono = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.cedula} {self.fecha_nacimiento} {self.genero} {self.correo} {self.telefono}"

class Registro(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now=True)
    frecuencia_cardiaca = models.IntegerField()
    frecuencia_respiratoria = models.IntegerField()
    presion_arterial_sistolica = models.IntegerField()
    presion_arterial_diastolica = models.IntegerField()
    saturacion_oxigeno = models.IntegerField()
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.paciente.nombre} {self.fecha_hora} {self.frecuencia_cardiaca} {self.frecuencia_respiratoria} {self.presion_arterial_sistolica} {self.presion_arterial_diastolica} {self.saturacion_oxigeno} {self.temperatura}"
    
class UbicacionDolor(models.Model):
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE, related_name='ubicaciones_dolor')
    ubicacion = models.CharField(max_length=50)  # e.g., "cabeza", "pecho", etc.
    tipo_dolor = models.CharField(max_length=50)  # e.g., "punzante", "ardor", "eléctrico"

    def __str__(self):
        return f"{self.ubicacion} {self.tipo_dolor}"
