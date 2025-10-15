from django.contrib import admin
from .models import Usuario, Projeto, Tarefa, Etiqueta, Comentario, Coluna
# Register your models here.

admin.register(Usuario)
admin.register(Projeto)
admin.register(Tarefa)
admin.register(Etiqueta)
admin.register(Comentario)
admin.register(Coluna)
