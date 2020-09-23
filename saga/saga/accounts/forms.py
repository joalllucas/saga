from django import forms
from django.contrib.auth import get_user_model
from .models import PasswordReset
from .utils import generate_hash_key
from .mail import send_mail_template
from PIL import Image
import datetime
from django.conf import settings
User = get_user_model()

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)
    course = forms.CharField(label='Curso', max_length=50)
    period = forms.IntegerField(label='Período')
    group = forms.CharField(label='Turma', max_length=10)
    ira = forms.FloatField(label='IRA')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        course = self.cleaned_data['course']
        period = self.cleaned_data['period']
        group = self.cleaned_data['group']
        ira = self.cleaned_data['ira']
        study_time_diary = self.cleaned_data['study_time_diary']

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'course', 'period', 'group', 'ira', 'study_time_diary']


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'course', 'period', 'group', 'ira', 'study_time_diary']


class EditImageForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['image', 'x', 'y', 'width', 'height']

    def save(self):
        user = super(EditImageForm, self).save()

        x = float(self.data.get('x'))
        y = float(self.data.get('y'))
        w = float(self.data.get('width'))
        h = float(self.data.get('height'))

        image = Image.open(user.image)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(user.image.path)

        return user

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário cadastrado com este e-mail.')

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'password_reset_mail.html'
        subject = 'Redefinição de senha'
        context = {
            'reset': reset,
            'user': user,
            'year': datetime.date.today().year
        }
        send_mail_template(subject, template_name, context, [user.email], from_email=settings.DEFAULT_FROM_EMAIL)