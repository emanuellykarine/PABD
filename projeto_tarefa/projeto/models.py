from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Projeto(models.Model):
    usuario = models.ForeignKey('Usuario', related_name='projetos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.nome}, {self.descricao}, {self.data_inicio}, {self.data_fim}"

class Tarefa(models.Model):
    projeto = models.ForeignKey(Projeto, related_name='tarefas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.titulo}, {self.descricao}, {self.data_criacao}, {self.data_conclusao}, {self.concluida}"

class Usuario(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"