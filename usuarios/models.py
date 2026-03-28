from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Usuario(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


#Models Google
class GoogleAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    google_sub = models.CharField(max_length=255, unique=True)
    picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Google"
