from django.db import models

PRIORIDADES = [('baixa', 'Baixa'), ('média', 'Média'), ('alta', 'Alta')]
# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f'{self.nome} {self.cpf}'
    
class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    proprietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='projetos_proprios')
    membros = models.ManyToManyField(Usuario, related_name='projetos_parte', blank=True)

    def __str__(self):
        return self.nome
    
class Coluna(models.Model):
    titulo = models.CharField(max_length=30)
    ordem = models.PositiveIntegerField(default=0) #é sempre um inteiro positivo, vai atribuir numero e assim o meta vai ordenar 
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='colunas') 

    class Meta: #vai ordenar por ordem dada no atributo ordem
        ordering = ['ordem']

    def __str__(self):
        return f"{self.titulo} ({self.projeto.nome})"

class Etiqueta(models.Model):
    nome = models.CharField(max_length=50)
    cor = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
class Tarefa(models.Model):
    titulo = models.CharField(max_length=30)
    descricao = models.TextField()
    coluna = models.ForeignKey(Coluna, on_delete=models.CASCADE, related_name='tarefas')
    responsavel = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL, related_name='tarefa_responsavel') #mesmo se o usuário for deletado a tarefa continua existindo
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tarefas_criadas')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADES, default="média")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Etiqueta, blank=True, related_name='tarefas')

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor.nome} em {self.tarefa.titulo}"

