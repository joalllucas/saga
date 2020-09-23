from django import forms
from saga.accounts.mail import send_mail_template
import datetime

class DeveloperContact(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assunto'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mensagem'}))

    def send_mail(self, request):
        subject = self.cleaned_data['subject']
        from_email = 'SAGA - ' + self.cleaned_data['name'] + ' <saga.mailsystem@gmail.com>'
        if request.POST['button'] == 'joao_lucas':
            send_to = 'jpaivapaulino@gmail.com'
            developer = 'Joao Lucas'
        context = {
            'name': self.cleaned_data['name'],
            'subject': self.cleaned_data['subject'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
            'developer': developer,
            'year': datetime.date.today().year,
        }
        template_name = 'developer_contact.html'
        send_mail_template(subject, template_name, context, [send_to], from_email)