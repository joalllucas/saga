from django.conf.urls import url

from saga.core.views import home, developers
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'desenvolvedores/$', developers, name='developers'),
]