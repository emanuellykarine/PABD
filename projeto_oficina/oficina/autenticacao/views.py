from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from .serializers import UsuarioRegistroSerializer, UsuarioPerfilSerializer
from .models import Usuario
# Create your views here.
#/api/auth/registro/ post
#/api/auth/login/ post
#/api/auth/logout/ post
#/api/auth/perfil/ get, put

class RegistroUsuarioView(APIView):
    def post(self, request):
        serializer = UsuarioRegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUsuarioView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            token, created = Token.objects.get_or_create(user=usuario)
            return Response({
                'token': token.key,
                'username': usuario.username,
                'tipo_perfil': usuario.tipo_perfil
            })
        else:
            return Response({'mensagem': 'Login ou Senha Inválido'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutUsuarioView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'detail': 'Usuário deslogado com sucesso.'})
        except Exception as e:
            return Response({'erro': 'Erro ao deslogar'}, status=status.HTTP_400_BAD_REQUEST)

class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        usuario = request.user
        serializer = UsuarioPerfilSerializer(usuario)
        return Response(serializer.data)

    def put(self, request):
        usuario = request.user
        serializer = UsuarioPerfilSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)