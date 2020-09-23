from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .decorators import user_is_owner
from .forms import NewSubject
from .models import Subject
from .slugify import slugify
import datetime
import requests
import json

def slug_define(name, slug_):
    slug = slugify(name)
    if slug == 'nova':
        raise forms.ValidationError('URL não permitido.')
    if Subject.object.filter(slug=slug):
        slug = slug_ + str(Subject.object.latest('id').id + 1)
    return slug

@login_required
def index(request):
    subjects = Subject.object.filter(owner=request.user)
    template_name = "subjects/index.html"
    context = {
        'subjects': subjects
    }
    color_list = ['aqua', 'blue', 'light-blue', 'teal', 'yellow', 'orange', 'green', 'lime', 'red', 'purple', 'fuchsia', 'navy']
    if request.method == 'POST':
        if request.POST['button'] == 'suap':
            username = str(request.POST['username_suap'])
            password = str(request.POST['password_suap'])
            url_token = 'https://suap.ifrn.edu.br/api/v2/autenticacao/token/'
            headers_token = {'content-type': 'application/json', 'Accept': 'application/json'}
            data = {"username": username, "password": password}
            response_token = requests.post(url_token, data=json.dumps(data), headers=headers_token)
            if 'token' in response_token.json():
                token = response_token.json()['token']
                year_suap = str(request.POST['year_suap'])
                period_suap = str(request.POST['period_suap'])
                if year_suap and period_suap:
                    url_report_card = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/' + year_suap + '/' + period_suap + '/'
                    url_groups = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turmas-virtuais/' + year_suap + '/' + period_suap + '/'
                else:
                    url_report_card = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/' + str(datetime.datetime.today().year) + '/1/'
                    url_groups = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turmas-virtuais/' + str(datetime.datetime.today().year) + '/1/'
                headers_geral = {'Authorization': 'JWT ' + token}
                response_report_card = requests.get(url_report_card, headers=headers_geral)
                response_groups = requests.get(url_groups, headers=headers_geral)
                x = 0
                for i in response_report_card.json():
                    id_suap = int(i['codigo_diario'])
                    subjects_suap = Subject.object.filter(owner=request.user, id_suap=id_suap)
                    if not subjects_suap:
                        name = i['disciplina']
                        slug = slugify(name)
                        workload = int(i['carga_horaria'])
                        if workload > 120:
                            if 'H)' in name:
                                r = -6
                            else:
                                r = None
                        else:
                            if 'H)' in name:
                                r = -5
                            else:
                                r = None
                        if workload > 50:
                            modality = False
                            if i['nota_etapa_1']['nota']:
                                note1 = int(i['nota_etapa_1']['nota'])
                            else:
                                note1 = None
                            if i['nota_etapa_2']['nota']:
                                note2 = int(i['nota_etapa_2']['nota'])
                            else:
                                note2 = None
                            if i['nota_etapa_3']['nota']:
                                note3 = int(i['nota_etapa_3']['nota'])
                            else:
                                note3 = None
                            if i['nota_etapa_4']['nota']:
                                note4 = int(i['nota_etapa_4']['nota'])
                            else:
                                note4 = None
                        else:
                            modality = True
                            if i['nota_etapa_1']['nota']:
                                note1 = int(i['nota_etapa_1']['nota'])
                            else:
                                note1 = None
                            if i['nota_etapa_2']['nota']:
                                note2 = int(i['nota_etapa_2']['nota'])
                            else:
                                note2 = None
                            note3 = None
                            note4 = None

                        for j in response_groups.json():
                            if str(id_suap) == j['id']:
                                if j['horarios_de_aula'] == '':
                                    schedule = 'suap '
                                else:
                                    schedule = 'suap'
                                    schedule_suap = j['horarios_de_aula']
                                    schedule_split = schedule_suap.split()
                                    for k in schedule_split:
                                        if len(k) >= 2:
                                            if k[1] == 'M':
                                                shift = 'm..'
                                            if k[1] == 'V':
                                                shift = 'v..'
                                            if k[1] == 'N':
                                                shift = 'n..'

                                            if k[0] == '1':
                                                day = 'sun.'
                                            if k[0] == '2':
                                                day = 'mon.'
                                            if k[0] == '3':
                                                day = 'tue.'
                                            if k[0] == '4':
                                                day = 'wed.'
                                            if k[0] == '5':
                                                day = 'thu.'
                                            if k[0] == '6':
                                                day = 'fri.'
                                            if k[0] == '7':
                                                day = 'sat.'

                                            schedule_temp = shift + day

                                            if len(k) == 3:
                                                schedule_parcial = schedule_temp + k[2]
                                            if len(k) == 4:
                                                schedule_parcial = schedule_temp + k[2] + schedule_temp + k[3]
                                            if len(k) == 5:
                                                schedule_parcial = schedule_temp + k[2] + schedule_temp + k[3] + schedule_temp + k[4]
                                            if len(k) == 6:
                                                schedule_parcial = schedule_temp + k[2] + schedule_temp + k[3] + schedule_temp + k[4] + schedule_temp + k[5]
                                            if len(k) == 7:
                                                schedule_parcial = schedule_temp + k[2] + schedule_temp + k[3] + schedule_temp + k[4] + schedule_temp + k[5] + schedule_temp + k[6]
                                            if len(k) == 8:
                                                schedule_parcial = schedule_temp + k[2] + schedule_temp + k[3] + schedule_temp + k[4] + schedule_temp + k[5] + schedule_temp + k[6] + schedule_temp + k[7]

                                        schedule = schedule + schedule_parcial

                        url_subject = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turma-virtual/' + str(id_suap) + '/'
                        response_diary = requests.get(url_subject, headers=headers_geral)
                        year = response_diary.json()['ano_letivo']
                        period = response_diary.json()['periodo_letivo']
                        period = year + '.' + period
                        teacher = response_diary.json()['professores'][0]['nome']

                        while x > 11:
                            x = x - 12

                        color = str(color_list[x])

                        form = NewSubject({
                            'id_suap': id_suap,
                            'owner': request.user.id,
                            'name': name[11:r],
                            'slug': slug_define(name, slug),
                            'interest': 5,
                            'modality': modality,
                            'color': color,
                            'note1': note1,
                            'note2': note2,
                            'note3': note3,
                            'note4': note4,
                            'period': period,
                            'teacher': teacher,
                            'group': request.user.group,
                            'schedule': schedule
                        })
                        if form.is_valid():
                            form.save()

                        x = x + 1

                context['success'] = True

            else:
                context['success'] = False

    return render(request, template_name, context)\

"""           
@login_required
def index(request):
    subjects = Subject.object.filter(owner=request.user)
    template_name = "subjects/index.html"
    context = {
        'subjects': subjects
    }
    color_list = ['aqua', 'blue', 'light-blue', 'teal', 'yellow', 'orange', 'green', 'lime', 'red', 'purple', 'fuchsia', 'navy']
    if request.method == 'POST':
        if request.POST['button'] == 'suap':
            username = str(request.POST['username_suap'])
            password = str(request.POST['password_suap'])
            url = 'https://suap.ifrn.edu.br/api/v2/autenticacao/token/'
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            data = {"username": username, "password": password}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            if 'token' in response.json():
                token = response.json()['token']
                year_suap = str(request.POST['year_suap'])
                period_suap = str(request.POST['period_suap'])
                if year_suap and period_suap:
                    url = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/' + year_suap + '/' + period_suap + '/'
                else:
                    url = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/' + str(datetime.datetime.today().year) + '/1/'
                headers = {'Authorization': 'JWT ' + token}
                response = requests.get(url, headers=headers)
                x = 0
                for i in response.json():
                    id_suap = int(i['codigo_diario'])
                    subjects_suap = Subject.object.filter(owner=request.user, id_suap=id_suap)
                    if not subjects_suap:
                        name = i['disciplina']
                        slug = slugify(name)
                        workload = int(i['carga_horaria'])
                        if workload > 120:
                            if 'H)' in name:
                                r = -6
                            else:
                                r = None
                        else:
                            if 'H)' in name:
                                r = -5
                            else:
                                r = None
                        if workload > 50:
                            modality = False
                            if i['nota_etapa_1']['nota']:
                                note1 = int(i['nota_etapa_1']['nota'])
                            else:
                                note1 = None
                            if i['nota_etapa_2']['nota']:
                                note2 = int(i['nota_etapa_2']['nota'])
                            else:
                                note2 = None
                            if i['nota_etapa_3']['nota']:
                                note3 = int(i['nota_etapa_3']['nota'])
                            else:
                                note3 = None
                            if i['nota_etapa_4']['nota']:
                                note4 = int(i['nota_etapa_4']['nota'])
                            else:
                                note4 = None
                        else:
                            modality = True
                            if i['nota_etapa_1']['nota']:
                                note1 = int(i['nota_etapa_1']['nota'])
                            else:
                                note1 = None
                            if i['nota_etapa_2']['nota']:
                                note2 = int(i['nota_etapa_2']['nota'])
                            else:
                                note2 = None
                            note3 = None
                            note4 = None

                        url = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turma-virtual/' + str(id_suap) + '/'
                        response_diary = requests.get(url, headers=headers)
                        year = response_diary.json()['ano_letivo']
                        period = response_diary.json()['periodo_letivo']
                        period = year + '.' + period
                        teacher = response_diary.json()['professores'][0]['nome']

                        while x > 11:
                            x = x - 12

                        color = str(color_list[x])

                        form = NewSubject({
                            'id_suap': id_suap,
                            'owner': request.user.id,
                            'name': name[11:r],
                            'slug': slug_define(name, slug),
                            'interest': 5,
                            'modality': modality,
                            'color': color,
                            'note1': note1,
                            'note2': note2,
                            'note3': note3,
                            'note4': note4,
                            'period': period,
                            'teacher': teacher,
                            'group': request.user.group,
                            'schedule': 'suap'
                        })
                        if form.is_valid():
                            form.save()

                        x = x + 1

                context['success'] = True

            else:
                context['success'] = False

    return render(request, template_name, context)
"""

#@login_required
#def details(request, pk):
#    subject = get_object_or_404(Subject, pk=pk)
#    context = {
#        'subject': subject
#    }
#    template_name = 'subjects/details.html'
#    return render(request, template_name, context)

@login_required
@user_is_owner
def details(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    context = {
        'subject': subject
    }
    template_name = 'subjects/details.html'
    if request.method == 'POST':
        subject.delete()
        return redirect('/disciplinas/')
    return render(request, template_name, context)

@login_required
def new(request):
    context = {}
    if request.method == 'POST':
        form = NewSubject(request.POST or None)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.owner = request.user
            context['is_valid'] = True
            form.save()
            form = NewSubject()
        else:
            context['is_valid'] = False
    else:
        form = NewSubject()

    context['form'] = form
    return render(request, 'subjects/new.html', context)

@login_required
@user_is_owner
def edit(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    context = {
        'subject': subject
    }
    template_name = 'subjects/edit.html'
    if request.method == 'POST':
        instance = get_object_or_404(Subject, slug=slug)
        form = NewSubject(request.POST, instance=instance)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.owner = request.user
            context['is_valid'] = True
            form.save()
        else:
            context['is_valid'] = False
    else:
        form = NewSubject()

    context['form'] = form
    return render(request, template_name, context)