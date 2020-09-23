from django.db import models
from saga.accounts.models import User
from saga.subjects.models import Subject

class TaskManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class Task(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)
    subject = models.ForeignKey(Subject)
    evaluation_type = models.CharField('Tipo de avaliação', max_length=100)
    title = models.CharField('Título', max_length=100)
    start = models.CharField('Início', max_length=100)
    start_date = models.DateField(blank=True)
    end = models.CharField('Fim', max_length=100)
    end_date = models.DateField(blank=True)
    color = models.CharField('Cor', max_length=10, blank=True)
    description = models.CharField('Descrição', max_length=900, blank=True, null=True)
    object = TaskManager()

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['start_date', 'title', 'id']