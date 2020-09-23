from django.conf.urls import url, include
from .views import index, tasks_feed

urlpatterns = [
    url(r'^',
        include([
            url(r'^$', index, name='index'),
            url(r'tasks_feed/', tasks_feed, name='tasks_feed'),
        ])),
]