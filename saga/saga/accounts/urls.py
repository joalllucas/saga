from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from saga.accounts.views import account, register, edit, change_password, password_reset, password_reset_confirm

urlpatterns = [
    url(r'^conta/',
        include([
            url(r'^$', account, name='account'),
            url(r'^editar/$', edit, name='edit'),
            url(r'^alterar-senha/$', change_password, name='change_password'),
        ])),
    url(r'^entrar/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^sair/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^cadastrar/$', register, name='register'),
    url(r'^recuperar-senha/$', password_reset, name='password_reset'),
    url(r'^confirmar-recuperar-senha/(?P<key>\w+)/$', password_reset_confirm, name='password_reset_confirm'),
]