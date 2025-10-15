from rest_framework import serializers
from .models import Projeto, Coluna, Tarefa, Etiqueta, Comentario, Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nome", "cpf"]


class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ['id', 'nome', 'cor']


class ComentarioSerializer(serializers.ModelSerializer):
    autor = UsuarioSerializer(read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'autor', 'texto', 'data_criacao']


class TarefaSerializer(serializers.ModelSerializer):
    responsavel_info = UsuarioSerializer(source='responsavel', read_only=True)
    criador_info = UsuarioSerializer(source='criador', read_only=True)
    responsavel = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), allow_null=True, required=False)
    criador = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    tags_nomes = serializers.SlugRelatedField( #vai mostrar o nome da tag ao inves do id é o nome relacionado
        source='tags',
        many=True,
        read_only=True,
        slug_field='nome'
    )
    tags = serializers.PrimaryKeyRelatedField(queryset=Etiqueta.objects.all(), many=True, required=False)
    comentarios_count = serializers.SerializerMethodField()

    class Meta:
        model = Tarefa
        fields = [
            'id', 'titulo', 'descricao', 'coluna', 'responsavel', 'responsavel_info', 
            'criador', 'criador_info', 'prioridade', 'data_criacao', 'data_conclusao', 
            'tags', 'tags_nomes', 'comentarios_count'
        ]

    def get_comentarios_count(self, obj):
        return obj.comentarios.count()


class ColunaSerializer(serializers.ModelSerializer):
    tarefas = TarefaSerializer(many=True, read_only=True)
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)
    projeto = serializers.PrimaryKeyRelatedField(queryset=Projeto.objects.all())

    class Meta:
        model = Coluna
        fields = ['id', 'titulo', 'ordem', 'projeto', 'projeto_nome', 'tarefas']

class ProjetoSerializer(serializers.ModelSerializer):
    colunas = ColunaSerializer(many=True, read_only=True)
    membros_nomes = serializers.SerializerMethodField() #É um campo que o serializer mostra, mas que não existe na tabela do banco cria ele “virtualmente” a partir de uma função
    tarefas_total = serializers.SerializerMethodField()

    class Meta:
        model = Projeto
        fields = [
            'id', 'nome', 'descricao', 'data_criacao',
            'proprietario', 'membros_nomes', 'colunas', 'tarefas_total'
        ]

    def get_membros_nomes(self, obj):
        return [membro.nome for membro in obj.membros.all()]

    def get_tarefas_total(self, obj):
        return sum(coluna.tarefas.count() for coluna in obj.colunas.all())
