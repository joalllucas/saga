from django.conf.urls import url, include
from .views import study_time

urlpatterns = [
    url(r'^',
        include([
            url(r'^$', study_time, name='study_time'),
        ])),
]