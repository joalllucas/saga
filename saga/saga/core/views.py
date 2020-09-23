from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from saga.subjects.models import Subject
from saga.tasks.models import Task
import datetime
from saga.study_time.views import day_studies
from .forms import DeveloperContact

@login_required
def home(request):
    subjects = Subject.object.filter(owner=request.user)
    critical = Subject.object.filter(owner=request.user, parcial_media__lt=60).count()

    date = datetime.date.today()
    if date.isoweekday() == 7:
        date = date + datetime.timedelta(1)
    start_week = date - datetime.timedelta(date.isoweekday())
    end_week = start_week + datetime.timedelta(6)
    week_tasks = Task.object.filter(owner=request.user).exclude(end_date__lt=start_week).exclude(start_date__gt=end_week)
    week_tasks_value = week_tasks.count()

    hours = request.user.study_time_diary
    daily_progresses = day_studies(datetime.date.today().weekday(), request)
    daily_progresses_value = len(daily_progresses)
    for daily_progress in daily_progresses:
        if daily_progresses_value == 1:
            subject = get_object_or_404(Subject, pk=daily_progress.id)
            subject.daily_goal = hours*1
            if not subject.edited.weekday() is datetime.date.today().weekday():
                subject.daily_progress = 0
            subject.save()
        elif daily_progresses_value == 2:
            if daily_progresses.index(daily_progress) == 0:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = hours * 0.6
                subject.save()
            elif daily_progresses.index(daily_progress) == 1:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = hours * 0.4
                if not subject.edited.weekday() is datetime.date.today().weekday():
                    subject.daily_progress = 0
                subject.save()
        elif daily_progresses_value == 3:
            if daily_progresses.index(daily_progress) == 0:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = hours * 0.5
                if not subject.edited.weekday() is datetime.date.today().weekday():
                    subject.daily_progress = 0
                subject.save()
            elif daily_progresses.index(daily_progress) == 1:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = hours * 0.3
                if not subject.edited.weekday() is datetime.date.today().weekday():
                    subject.daily_progress = 0
                subject.save()
            elif daily_progresses.index(daily_progress) == 2:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = hours * 0.2
                if not subject.edited.weekday() is datetime.date.today().weekday():
                    subject.daily_progress = 0
                subject.save()
        else:
            if daily_progresses.index(daily_progress) == 0:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = hours * 0.4
                if not subject.edited.weekday() is datetime.date.today().weekday():
                    subject.daily_progress = 0
                subject.save()
            elif daily_progresses.index(daily_progress) == 1:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = hours * 0.3
                if not subject.edited.weekday() is datetime.date.today().weekday():
                    subject.daily_progress = 0
                subject.save()
            elif daily_progresses.index(daily_progress) == 2:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = hours * 0.2
                if not subject.edited.weekday() is datetime.date.today().weekday():
                    subject.daily_progress = 0
                subject.save()
            else:
                subject = get_object_or_404(Subject, pk=daily_progress.id)
                subject.daily_goal = 0.5
                if not subject.edited.weekday() is datetime.date.today().weekday():
                    subject.daily_progress = 0
                subject.save()

    if request.method == 'POST':
        slug = request.POST['button']
        daily_progress_input = 'daily_progress_' + slug
        subject = get_object_or_404(Subject, slug=slug)
        subject.daily_progress = request.POST[daily_progress_input]
        subject.edited = datetime.datetime.now() - datetime.timedelta(hours=3)
        subject.save()
        return redirect('/')

    daily_total = 0
    daily_total_hours = 0
    for daily_progress in daily_progresses:
        daily_total = daily_total + daily_progress.daily_progress/daily_progress.daily_goal
        daily_total_hours = daily_total_hours + daily_progress.daily_progress
    if daily_progresses_value:
        daily_total = int(daily_total/daily_progresses_value * 100)

    context = {'subjects': subjects}
    context['critical'] = critical
    context['week_tasks'] = week_tasks
    context['week_tasks_value'] = week_tasks_value
    context['daily_progresses'] = daily_progresses
    context['daily_progresses_value'] = daily_progresses_value
    context['daily_total'] = daily_total
    context['daily_total_hours'] = daily_total_hours
    return render(request, 'home.html', context)

def developers(request):
    context = {}
    form = DeveloperContact(request.POST or None)
    if form.is_valid():
        form.send_mail(request)
        context['success'] = True
        form = DeveloperContact()
    context['form'] = form
    return render(request, 'developers.html', context)

def bad_request(request):
    response = render_to_response(request, '400.html')
    response.status_code = 400
    return response

def permission_denied(request):
    response = render(request, '403.html')
    response.status_code = 403
    return response

def page_not_found(request):
    response = render_to_response(request, '404.html')
    response.status_code = 404
    return response

def server_error(request):
    response = render_to_response(request, '500.html')
    response.status_code = 500
    return response