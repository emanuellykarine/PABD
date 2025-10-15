from rest_framework import serializers
from .models import Formulario, FormularioQuestao

class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = '__all__'

class FormularioQuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormularioQuestao
        fields ='__all__'