from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.serializers.json import json
from django.shortcuts import render
from .models import Task
from .forms import NewTask
from saga.subjects.models import Subject

@login_required
def index(request):
    tasks = Task.object.filter()
    context = {
        'tasks': tasks
    }
    subjects = Subject.object.filter(owner=request.user)
    context['subjects'] = subjects
    if request.method == 'POST':
        form = NewTask(request.POST or None)
        if request.POST['button'] == 'new':
            if form.is_valid():
                context['is_valid'] = True
                form.save()
                form = NewTask()
            else:
                context['is_valid'] = False

        if request.POST['button'] == 'edit':
            instance = Task.object.filter(pk=request.POST['id']).first()
            form = NewTask(request.POST, instance=instance)
            if form.is_valid():
                context['is_valid'] = True
                form.save()
            else:
                context['is_valid'] = False

        if request.POST['button'] == 'exclude':
            task = Task.object.filter(pk=request.POST['id']).first()
            task.delete()
    else:
        form = NewTask()
    first_subject = Subject.object.filter(owner=request.user).first()
    context['first_subject'] = first_subject
    context['form'] = form
    return render(request, 'index.html', context)

@login_required
def tasks_feed(request):
    tasks = Task.object.filter()
    json_list = []
    for task in tasks:
        if task.owner.id == request.user.id:
            id = task.id
            owner = task.owner.id
            subject = task.subject.id
            evaluation_type = task.evaluation_type
            title = task.title
            start = task.start
            end = task.end
            color = task.color
            description = task.description

            json_entry = {'id': id, 'owner': owner, 'subject': subject, 'evaluation_type': evaluation_type, 'title': title, 'start': start, 'end': end, 'color': color, 'description': description}
            json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')