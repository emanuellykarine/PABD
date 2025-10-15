from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Projeto, Coluna, Tarefa, Comentario, Usuario, Etiqueta
from .serializers import (
    ProjetoSerializer, ColunaSerializer, TarefaSerializer, ComentarioSerializer, UsuarioSerializer, EtiquetaSerializer
)

class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer

    @action(detail=True, methods=['post'])
    def add_membro(self, request, pk=None):
        """
        POST /api/projetos/{id}/add_membro/
        Body: {"user_id": 5}
        """
        projeto = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            usuario = Usuario.objects.get(id=user_id)
            projeto.membros.add(usuario)
            
            return Response({
                "message": f"{usuario.nome} adicionado ao projeto {projeto.nome}",
                "projeto_id": projeto.id,
                "novo_membro": usuario.nome,
                "total_membros": projeto.membros.count()
            })
        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
    @action(detail=True, methods=['get'])
    def minhas_tarefas(self, request, pk=None):
        """
        GET /api/projetos/{id}/minhas_tarefas/
        Query params: ?user_id=3 (opcional, se não informado usa o usuário logado)
        """
        projeto = self.get_object()
        user_id = request.query_params.get('user_id')
        
        try:
            usuario = Usuario.objects.get(id=user_id)
            
            # Buscar tarefas do usuário neste projeto
            tarefas = Tarefa.objects.filter(
                coluna__projeto=projeto,
                responsavel=usuario
            ).select_related('coluna', 'responsavel', 'criador')
            
            # Agrupar por coluna
            tarefas_por_coluna = {}
            for tarefa in tarefas:
                coluna_nome = tarefa.coluna.titulo
                if coluna_nome not in tarefas_por_coluna:
                    tarefas_por_coluna[coluna_nome] = []
                
                tarefas_por_coluna[coluna_nome].append({
                    "id": tarefa.id,
                    "titulo": tarefa.titulo,
                    "descricao": tarefa.descricao,
                    "prioridade": tarefa.prioridade,
                    "data_criacao": tarefa.data_criacao,
                    "data_conclusao": tarefa.data_conclusao,
                })
            
            return Response({
                "projeto": projeto.nome,
                "usuario": usuario.nome,
                "total_tarefas": tarefas.count(),
                "tarefas_por_coluna": tarefas_por_coluna,
                "estatisticas": {
                    "concluidas": tarefas.filter(data_conclusao__isnull=False).count(),
                    "em_andamento": tarefas.filter(data_conclusao__isnull=True).count(),
                    "alta_prioridade": tarefas.filter(prioridade="alta").count(),
                }
            })
            
        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
class ColunaViewSet(viewsets.ModelViewSet):
    queryset = Coluna.objects.all()
    serializer_class = ColunaSerializer


class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchBackend]
    filterset_fields = ['prioridade', 'coluna', 'responsavel', 'criador']
    search_fields = ['titulo', 'descricao']

    @action(detail=True, methods=['post'])
    def atribuir(self, request, pk=None):
        """
        POST /api/tarefas/{id}/atribuir/
        Body: {"user_id": 5}
        """
        tarefa = self.get_object()
        user_id = request.data.get('user_id')

        try:
            usuario = Usuario.objects.get(id=user_id)
            tarefa.responsavel = usuario
            tarefa.save()
            
            return Response({
                "message": f"Tarefa atribuída para {usuario.nome}",
                "tarefa_id": tarefa.id,
                "responsavel": usuario.nome
            })
        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer