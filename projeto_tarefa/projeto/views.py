from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Projeto, Tarefa, Usuario
from .serializers import ProjetoSerializer, TarefaSerializer, UsuarioSerializer

# Create your views here.

class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'descricao']

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'descricao']

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
