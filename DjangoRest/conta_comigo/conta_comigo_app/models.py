from django.db import models
from .choices import TIPO_DE_AUXILIO, SOLICITADOS_CHOICES, TIPO_PERGUNTA_CHOICES
from django.core.exceptions import ValidationError

# Create your models here.
class Formulario(models.Model):
    titulo = models.CharField(max_length=100)
    objetivo = models.TextField()
    tipo = models.CharField(max_length=30, choices=TIPO_DE_AUXILIO, default="auxilio transporte")
    solicitados = models.CharField(max_length=30, choices=SOLICITADOS_CHOICES, default="todos")
    data_inicio = models.DateField()
    data_fim = models.DateField()
    total_formulario = models.IntegerField() # total respondido?
    alunos_solicitados = models.IntegerField()
    sem_resposta = models.IntegerField()

    def __str__(self):
        return f"{self.titulo} - {self.objetivo}"

    def clean(self):
        erros = {}
        if self.titulo == "":
            erros['titulo'] = "O formulário deve ter um título"
        if self.data_fim < self.data_inicio:
            erros['data fim'] = "A data do fim  do formulário não pode ser menor que a data inicial"

        # if self.data_fim <= timezone.datetime.now().date:
        #     erros['data fim'] = "A data do fim do formulário pode ser posterior a hoje."

        if erros:
            raise ValidationError(erros)

    class Meta:
        db_table = 'formulario'

class FormularioQuestao(models.Model):
    formulario = models.ForeignKey('Formulario', on_delete=models.CASCADE, related_name='questoes')
    titulo_pergunta = models.CharField(max_length=250)
    tipo_pergunta = models.CharField(max_length=50, choices=TIPO_PERGUNTA_CHOICES, default='multipla escolha')
    obrigatoriedade = models.BooleanField()
    ordem = models.PositiveIntegerField(default=0) #para ordenar as questões no formulário

    class Meta:
        db_table = 'formulario_questao'
        ordering = ['ordem']

    def __str__(self):
        return f"{self.titulo_pergunta} ({self.get_tipo_pergunta_display()})"

    def clean(self):
        erros = {}
        if not self.titulo_pergunta or len(self.titulo_pergunta) < 5:
            erros['titulo_pergunta'] = "A pergunta deve ter um título com pelo menos 5 caracteres."
        if erros:
            raise ValidationError(erros)
