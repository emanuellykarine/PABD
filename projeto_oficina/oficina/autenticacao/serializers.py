#UsuarioRegistroSerializer: Para cadastro (validação de CPF, senha forte)
#LoginSerializer: Para autenticação
#UsuarioPerfilSerializer: Para visualização/edição de perfil
from rest_framework import serializers
from .models import Usuario

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirmar_senha = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'cpf', 'telefone', 'tipo_perfil', 'senha', 'confirmar_senha']
        read_only_fields = ['id']
    
    def validate_cpf(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("CPF deve conter exatamente 11 dígitos numéricos.")
        return value
    
    def validate(self, data):
        if data['senha'] != data['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirmar_senha')
        senha = validated_data.pop('senha')
        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        return usuario
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    senha = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'cpf', 'telefone', 'tipo_perfil', 'data_cadastro', 'ativo']
        read_only_fields = ['id', 'data_cadastro']

    def update(self, instance, validated_data):
        senha = validated_data.pop('senha', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if senha:
            instance.set_password(senha)
        instance.save()
        return instance