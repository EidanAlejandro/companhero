from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class EstadoPerfil(models.Model):
    id_estado_perfil = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre_estado

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    id_estado_perfil = models.ForeignKey(EstadoPerfil, on_delete=models.CASCADE)
    nombre_perfil = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre_perfil

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# CAMBIO IMPORTANTE: No usar AbstractBaseUser por ahora
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_direccion = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre_direccion