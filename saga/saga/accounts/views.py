from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, EditAccountForm, PasswordResetForm, EditImageForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import PasswordReset
import requests
import json

User = get_user_model()

@login_required
def account(request):
    return render(request, 'account.html')

def register(request):
    def word_count(string):
        tokens = string.split()
        n_tokens = len(tokens)
        return n_tokens

    template_name = 'register.html'
    context = {}
    if request.method == 'POST':
        if request.POST['button'] == 'suap':
            username = str(request.POST['username_suap'])
            password = str(request.POST['password_suap'])
            url = 'https://suap.ifrn.edu.br/api/v2/autenticacao/token/'
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            data = {"username": username, "password": password}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            if 'token' in response.json():
                form = RegisterForm()
                token = response.json()['token']

                url = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/'
                headers = {'Authorization': 'JWT ' + token}
                response = requests.get(url, headers=headers)
                bond = str(response.json()['tipo_vinculo'])
                if bond == 'Aluno':
                    name = str(response.json()['vinculo']['nome'])
                    first_name1 = name.split(' ')[0]
                    first_name2 = name.split(' ')[1]
                    first_name = first_name1 + ' ' + first_name2
                    name_count = word_count(name) - 2
                    last_name = ''
                    for x in range(name_count):
                        x = x + 1
                        name_temp = name.split(' ')[-x]
                        last_name = name_temp + ' ' + last_name
                    email = response.json()['email']
                    course = str(response.json()['vinculo']['curso'])

                    url = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-periodos-letivos/'
                    response = requests.get(url, headers=headers)
                    period = len(response.json())

                    context['form'] = form
                    context['token'] = token
                    context['username'] = int(username)
                    context['password'] = password
                    context['first_name'] = first_name
                    context['last_name'] = last_name
                    context['email'] = email
                    context['course'] = course
                    context['period'] = period
                else:
                    context['username'] = int(username)
                    context['password'] = password
            else:
                context['error'] = 'Matrícula e senha não conferem.'

        elif request.POST['button'] == 'save':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/entrar/')
            else:
                context['is_valid'] = False
                context['form'] = form

    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        image_form = EditImageForm(request.POST, request.FILES, instance=request.user)
        if request.POST['button'] == 'save':
            if form.is_valid():
                form.save()
                form = EditAccountForm(instance=request.user)
                context['success'] = True
            else:
                context['success'] = False
            image_form = EditImageForm(instance=request.user)
        if request.POST['button'] == 'save_image':
            if image_form.is_valid():
                image_form.save()
                image_form = EditImageForm(instance=request.user)
                context['success'] = True
            else:
                context['success'] = False
            form = EditAccountForm(instance=request.user)
    else:
        form = EditAccountForm(instance=request.user)
        image_form = EditImageForm(instance=request.user)
    context['form'] = form
    context['image_form'] = image_form
    return render(request, template_name, context)

@login_required
def change_password(request):
    template_name = 'change_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
        else:
            context['success'] = False
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)

def password_reset(request):
    template_name = 'password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)