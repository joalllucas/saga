from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'id'] #Define campos exibidos no CRUD
    search_fields = ['title'] #Define campos que serão pesquisados pelo CRUD

admin.site.register(Task, TaskAdmin)