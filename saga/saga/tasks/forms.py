import datetime
from .models import Task
from django.forms import ModelForm
from saga.subjects.models import Subject

class NewTask(ModelForm):
    class Meta:
        model = Task
        fields = ['owner', 'subject', 'evaluation_type', 'title', 'start', 'start_date', 'end', 'end_date', 'color', 'description']

    def clean_color(self):
        colorFinal = ''
        subject = self.cleaned_data['subject']
        if subject is not None:
            subjectId = self.cleaned_data['subject'].id
            subject = Subject.object.filter(pk=subjectId).first()
            color = subject.color
            if color == 'aqua':
                colorFinal = '#00c0ef'
            if color == 'blue':
                colorFinal = '#0073b7'
            if color == 'light-blue':
                colorFinal = '#3c8dbc'
            if color == 'teal':
                colorFinal = '#39CCCC'
            if color == 'yellow':
                colorFinal = '#f39c12'
            if color == 'orange':
                colorFinal = '#ff851b'
            if color == 'green':
                colorFinal = '#00a65a'
            if color == 'lime':
                colorFinal = '#01FF70'
            if color == 'red':
                colorFinal = '#f56954'
            if color == 'purple':
                colorFinal = '#605ca8'
            if color == 'fuchsia':
                colorFinal = '#F012BE'
            if color == 'navy':
                colorFinal = '#001F3F'
        return colorFinal