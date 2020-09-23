from django.conf.urls import include, url
from saga.subjects.views import index, details, new, edit

urlpatterns = [
    url(r'^$', index, name='index'),
    #url(r'^(?P<pk>\d+)/', details, name='details'),
    url(r'^nova/$', new, name='new'),
    url(r'^(?P<slug>[\w_-]+)/', include([
        url(r'^$', details, name='details'),
        url(r'^editar/$', edit, name='edit'),
        ])),
]