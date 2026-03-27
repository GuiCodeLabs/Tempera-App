from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    pass

# Create your models here.
