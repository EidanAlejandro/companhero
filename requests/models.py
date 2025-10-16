from django.db import models
from surveys.models import Encuesta, Pregunta
from organization.models import JefeCuadrilla, Territorial

class EstadoSolicitud(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre_estado

class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    id_encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    id_cuadrilla = models.ForeignKey(JefeCuadrilla, on_delete=models.CASCADE)
    id_territorial = models.ForeignKey(Territorial, on_delete=models.CASCADE)
    id_estado = models.ForeignKey(EstadoSolicitud, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Solicitud {self.id_solicitud} - {self.fecha}"

class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    id_pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    respuesta = models.TextField()
    
    def __str__(self):
        return f"Respuesta {self.id_respuesta}"

class Multimedia(models.Model):
    TIPOS_MULTIMEDIA = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('documento', 'Documento'),
    ]
    
    id_multimedia = models.AutoField(primary_key=True)
    id_respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_MULTIMEDIA)
    archivo = models.FileField(upload_to='multimedia/')
    
    def __str__(self):
        return f"Multimedia {self.id_multimedia} - {self.tipo}"
