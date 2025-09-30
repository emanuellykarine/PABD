from rest_framework import serializers
from .models import Cliente

# transforma em bytes para ser armazenado ou transmitido para um banco de dados.
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__' 