from django.core.exceptions import PermissionDenied
from .models import Subject

def user_is_owner(function):
    def wrap(request, *args, **kwargs):
        subject = Subject.object.get(slug=kwargs['slug'])
        if subject.owner == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap