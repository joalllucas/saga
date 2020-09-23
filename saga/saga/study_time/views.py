from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from saga.subjects.models import Subject
from saga.tasks.models import Task
from itertools import chain
import datetime
from datetime import timedelta

@login_required
def study_time(request):
    subjects = variables('subjects', request)
    tasks = variables('tasks', request)

    week_studies = list(chain(day_studies(0, request), day_studies(1, request), day_studies(2, request), day_studies(3, request), day_studies(4, request), day_studies(5, request), day_studies(6, request)))

    context = {'subjects': subjects}
    context['tasks'] = tasks
    context['sun_studies'] = day_studies(6, request)
    context['mon_studies'] = day_studies(0, request)
    context['tue_studies'] = day_studies(1, request)
    context['wed_studies'] = day_studies(2, request)
    context['thu_studies'] = day_studies(3, request)
    context['fri_studies'] = day_studies(4, request)
    context['sat_studies'] = day_studies(5, request)
    context['week_studies'] = week_studies
    return render(request, 'study_time.html', context)

def day_studies(week_day, request):
    subjects = variables('subjects', request)
    tasks = variables('tasks', request)

    subjects_list = [list(subjects.filter(schedule__icontains='..mon.')), list(subjects.filter(schedule__icontains='..tue.')), list(subjects.filter(schedule__icontains='..wed.')), list(subjects.filter(schedule__icontains='..thu.')), list(subjects.filter(schedule__icontains='..fri.')), list(subjects.filter(schedule__icontains='..sat.')), list(subjects.filter(schedule__icontains='..sun.'))]
    tasks_subjects_list = tasks_subjects(week_day, 0, subjects, tasks)
    studies_prev = list()
    if tasks_subjects_list:
        for tasks_subject in tasks_subjects_list:
            if not tasks_subject in subjects_list[week_day] and not tasks_subject in studies_prev:
                studies_prev = list(chain(studies_prev, [tasks_subject]))
        studies = list(chain(subjects_list[week_day], studies_prev))
        studies = sorted(studies, key=lambda x: x.interest, reverse=True)
        studies = sorted(studies, key=lambda x: (x.parcial_media is None, x.parcial_media))
    else:
        studies = list(chain(subjects_list[week_day]))
    studies = sorted(studies, key=lambda x: x.interest, reverse=True)
    studies = sorted(studies, key=lambda x: (x.parcial_media is None, x.parcial_media))
    size_subjects = len(subjects_list[week_day])
    for tasks_subject in tasks_subjects_list:
        if len(studies) > 3:
            if len(studies) > size_subjects:
                for sat_subject in subjects_list[week_day]:
                    if not sat_subject in tasks_subjects_list:
                        del studies[studies.index(sat_subject)]
                        del subjects_list[week_day][subjects_list[week_day].index(sat_subject)]
    return studies

def tasks_subjects(week_day, key, subjects, tasks):
    if week_day == 6:
        week_day = 0
    else:
        week_day = week_day + 1
    tasks_list = list()
    tasks_subjects_list = list()
    for subject in subjects:
        for task in tasks:
            if task.subject.id == subject.id:
                start_date = task.start_date
                end_date = task.end_date
                delta = end_date - start_date
                for i in range(delta.days + 1):
                    date = start_date + timedelta(days=i)
                    if date.weekday() == week_day:
                        if not subject in tasks_list:
                            tasks_list = list(chain(tasks_list, [task]))
                            tasks_subjects_list = list(chain(tasks_subjects_list, [subject]))

    if key == 1:
        return tasks_list
    elif key == 0:
        return tasks_subjects_list

def variables(key, request):
    date = datetime.date.today()
    if date.isoweekday() == 7:
        date_week = date + datetime.timedelta(1)
    else:
        date_week = date
    start_week = date_week - datetime.timedelta(date_week.weekday())
    end_week = start_week + datetime.timedelta(6)

    subjects = Subject.object.filter(owner=request.user)
    tasks = Task.object.filter(owner=request.user).exclude(end_date__lt=start_week).exclude(start_date__gt=end_week)

    if key == 'subjects':
        return subjects
    elif key == 'tasks':
        return tasks