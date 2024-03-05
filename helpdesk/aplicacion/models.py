from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    descripcion = models.TextField(max_length=255)

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    comuna = models.TextField(max_length=255)

class Tecnico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    nivel = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PhotoBook(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photos = models.ManyToManyField(Photo)

class Estado(models.Model):
    nombre = models.TextField(max_length=255)

class Ticket(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    asunto = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=255)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    num_respuestas = models.IntegerField()
    tecnico_asig = models.ForeignKey(Tecnico, on_delete=models.CASCADE, null=True, blank=True)
    fecha_solucion = models.DateTimeField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    tiempo_dedicado = models.DateTimeField(null=True, blank=True)

class Respuesta(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE)
    respuesta = models.TextField(max_length=255)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

