from django.contrib import admin
from .models import User, PasswordReset

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'email', 'group']  # Define campos exibidos no CRUD
    search_fields = ['username', 'first_name', 'last_name']  # Define campos que serão pesquisados pelo CRUD
admin.site.register(User, UserAdmin)

class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ['user', 'key']  # Define campos exibidos no CRUD
    search_fields = ['user']  # Define campos que serão pesquisados pelo CRUD
admin.site.register(PasswordReset, PasswordResetAdmin)