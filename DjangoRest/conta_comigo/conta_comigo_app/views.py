from django.shortcuts import render
from rest_framework import viewsets
from .models import Formulario, FormularioQuestao
from .serializers import FormularioSerializer, FormularioQuestaoSerializer

class FormularioViewSet(viewsets.ModelViewSet):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer 

class FormularioQuestaoViewSet(viewsets.ModelViewSet):
    queryset = FormularioQuestao.objects.all()
    serializer_class = FormularioQuestaoSerializer