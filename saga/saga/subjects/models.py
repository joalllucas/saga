from django.db import models
from saga.accounts.models import User

class SubjectManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(name__icontains=query)

class Subject(models.Model):
    id_suap = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(User, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    period = models.CharField(max_length=6, blank=True)
    teacher = models.CharField(max_length=50)
    group = models.CharField(max_length=10)
    interest = models.IntegerField()
    modality = models.BooleanField()
    color = models.CharField(max_length=10)
    note1 = models.IntegerField(blank=True, null=True)
    note2 = models.IntegerField(blank=True, null=True)
    note3 = models.IntegerField(blank=True, null=True)
    note4 = models.IntegerField(blank=True, null=True)
    parcial_media = models.IntegerField(blank=True, null=True)
    media = models.IntegerField(blank=True, null=True)
    final_evaluation = models.IntegerField(blank=True, null=True)
    observations = models.TextField(blank=True)
    schedule = models.CharField(max_length=900)
    daily_goal = models.FloatField(default=1)
    daily_progress = models.FloatField(default=0)
    edited = models.DateTimeField(blank=True, null=True)
    object = SubjectManager()

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('subjects:details', (), {'slug': self.slug})

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ['owner', 'name', 'group', 'teacher']