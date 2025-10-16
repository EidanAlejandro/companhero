from django.db import models
from users.models import Usuario, Direccion

class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    id_direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_departamento = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_departamento

class Territorial(models.Model):
    id_territorial = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Territorial {self.id_territorial} - {self.id_usuario}"

class JefeCuadrilla(models.Model):
    id_cuadrilla = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Jefe Cuadrilla {self.id_cuadrilla} - {self.id_usuario}"
