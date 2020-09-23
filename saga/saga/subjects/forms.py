from .models import Subject
from django.forms import ModelForm
from django import forms
from .slugify import slugify
import datetime

class NewSubject(ModelForm):
    name = forms.CharField(label='Disciplina', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Disciplina', 'onchange': 'slugDefine()', 'onkeyup': 'slugDefine()'}))
    slug = forms.CharField(label='URL', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL', 'readonly': 'true'}))
    period = forms.CharField(label='Período', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Período'}))
    teacher = forms.CharField(label='Professor', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Professor'}))
    group = forms.CharField(label='Turma', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Turma'}))
    interest = forms.IntegerField(label='Nível de interesse', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nível de interesse', 'step': '1', 'min': '0', 'max': '10'}))
    color = forms.CharField(label='Cor')
    schedule = forms.CharField(label='Horário de aula')

    class Meta:
        model = Subject
        fields = ['id_suap', 'owner', 'name', 'slug', 'period', 'teacher', 'group', 'interest', 'modality', 'color', 'note1', 'note2', 'note3', 'note4', 'parcial_media', 'media', 'final_evaluation', 'observations', 'schedule', 'edited']

    def clean_interest(self):
        interest = self.cleaned_data['interest']
        if interest > 10 or interest < 0:
            raise forms.ValidationError('Informe um número de 0 a 10.')
        return interest

    def clean_note1(self):
        note1 = self.cleaned_data['note1']
        if note1:
            if note1 > 100 or note1 < 0:
                raise forms.ValidationError('Informe um número de 0 a 100.')
        return note1

    def clean_note2(self):
        note2 = self.cleaned_data['note2']
        if note2:
            if note2 > 100 or note2 < 0:
                raise forms.ValidationError('Informe um número de 0 a 100.')
        return note2

    def clean_note3(self):
        note3 = self.cleaned_data['note3']
        if note3:
            if note3 > 100 or note3 < 0:
                raise forms.ValidationError('Informe um número de 0 a 100.')
        return note3

    def clean_note4(self):
        note4 = self.cleaned_data['note4']
        if note4:
            if note4 > 100 or note4 < 0:
                raise forms.ValidationError('Informe um número de 0 a 100.')
        return note4

    def clean_parcial_media(self):
        note1 = self.cleaned_data['note1']
        note2 = self.cleaned_data['note2']
        note3 = self.cleaned_data['note3']
        note4 = self.cleaned_data['note4']
        modality = self.cleaned_data['modality']
        parcial_media = None
        if note1 or note1 == 0:
                parcial_media = note1
        if (note1 or note1 == 0) and (note2 or note2 == 0):
            if modality is True:
                parcial_media = int(((note1 * 2) + (note2 * 3)) / 5)
            else:
                parcial_media = int(((note1 * 2) + (note2 * 2)) / 4)
        if (note1 or note1 == 0) and (note2 or note2 == 0) and (note3 or note3 == 0):
            parcial_media = int(((note1 * 2) + (note2 * 2) + (note3 * 3)) / 7)
        if (note1 or note1 == 0) and (note2 or note2 == 0) and (note3 or note3 == 0) and (note4 or note4 == 0):
            parcial_media = int(((note1 * 2) + (note2 * 2) + (note3 * 3) + (note4 * 3)) / 10)
        return parcial_media

    def clean_media(self):
        note1 = self.cleaned_data['note1']
        note2 = self.cleaned_data['note2']
        note3 = self.cleaned_data['note3']
        note4 = self.cleaned_data['note4']
        modality = self.cleaned_data['modality']
        media = None
        if (note1 or note1 == 0) and (note2 or note2 == 0):
            if modality is True:
                media = int(((note1 * 2) + (note2 * 3)) / 5)
            else:
                if (note3 or note3 == 0) and (note4 or note4 == 0):
                    media = int(((note1 * 2) + (note2 * 2) + (note3 * 3) + (note4 * 3)) / 10)
        return media

    def clean_final_evaluation(self):
        note1 = self.cleaned_data['note1']
        note2 = self.cleaned_data['note2']
        media = self.cleaned_data['media']
        final_evaluation = None
        if media:
            if media < 60:
                final_evaluation1 = 120 - media
                final_evaluation2 = (300 - 3 * note2) / 2
                final_evaluation3 = (300 - 2 * note1) / 3
                if final_evaluation1 < final_evaluation2 and final_evaluation1 < final_evaluation3:
                    final_evaluation = final_evaluation1
                if final_evaluation2 < final_evaluation1 and final_evaluation2 < final_evaluation3:
                    final_evaluation = final_evaluation2
                if final_evaluation3 < final_evaluation1 and final_evaluation3 < final_evaluation2:
                    final_evaluation = final_evaluation3
        return final_evaluation

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug == 'nova':
            raise forms.ValidationError('URL não permitido.')
        if Subject.object.filter(slug=slug).exclude(slug=self.instance.slug).exists():
            slug = self.cleaned_data['slug'] + str(Subject.object.latest('id').id+1)
        return slug

    def clean_edited(self):
        edited = datetime.datetime.now() - datetime.timedelta(hours=3)
        return edited