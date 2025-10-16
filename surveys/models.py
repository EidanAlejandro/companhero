from django.db import models
from organization.models import Departamento

class TipoEncuesta(models.Model):
    id_tipo_encuesta = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_tipo

class Encuesta(models.Model):
    id_encuesta = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    id_tipo_encuesta = models.ForeignKey(TipoEncuesta, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.titulo

class Pregunta(models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    id_encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    texto_pregunta = models.TextField()
    
    def __str__(self):
        return self.texto_pregunta[:50]  # Muestra solo los primeros 50 caracteres