from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Projeto, Tarefa, Usuario
from .serializers import ProjetoSerializer, TarefaSerializer, UsuarioSerializer
from rest_framework.decorators import authentication_classes, permission_classes, api_view # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.authentication import TokenAuthentication, SessionAuthentication # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore

# Create your views here.

class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all() 
    serializer_class = ProjetoSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas os projetos do usuário logado"""
        return Projeto.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        """Ao criar um projeto, associa automaticamente ao usuário logado"""
        serializer.save(usuario=self.request.user)

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

@api_view(['POST'])
def login(request):
    user = get_object_or_404(Usuario, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'message': 'Not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuarioSerializer(instance=user)
    return Response({'token': token.key, 'user':serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = Usuario.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user':serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passou para {}".format(request.user.email))