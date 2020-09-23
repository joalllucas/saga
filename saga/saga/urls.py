"""saga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('saga.core.urls', namespace='core')),
    url(r'^', include('saga.accounts.urls', namespace='accounts')),
    url(r'^disciplinas/', include('saga.subjects.urls', namespace='subjects')),
    url(r'^tarefas/', include('saga.tasks.urls', namespace='tasks')),
    url(r'^horario-de-estudo/', include('saga.study_time.urls', namespace='study_time')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'saga.core.views.bad_request'
handler403 = 'saga.core.views.permission_denied'
handler404 = 'saga.core.views.page_not_found'
handler500 = 'saga.core.views.server_error'