from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    tipo_perfil = models.CharField(max_length=10, choices=[
        ('GERENTE', 'Gerente'),
        ('MECANICO', 'Mecânico'),
        ('CLIENTE', 'Cliente'),
    ])
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

