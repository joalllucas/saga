import re
from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Matrícula', max_length=14, unique=True, validators=[validators.RegexValidator(re.compile('[0-9]'), 'A matrícula só pode conter números.', 'invalid')])
    email = models.EmailField('E-mail', unique=True)
    first_name = models.CharField('Nome', max_length=50)
    last_name = models.CharField('Sobrenome', max_length=70)
    course = models.CharField('Curso', max_length=100)
    period = models.IntegerField('Período', null=True)
    group = models.CharField('Turma', max_length=10)
    ira = models.FloatField('IRA', null=True)
    study_time_diary = models.FloatField('Tempo de estudo diário')
    image = models.ImageField(upload_to='images/users/', blank=True, null=True)

    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='resets')
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at =  models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Reset de Senha'
        verbose_name_plural = 'Resets de Senhas'
        ordering = ['-created_at']