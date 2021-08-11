from functools import wraps

from django.shortcuts import redirect
from .utils import get_membership

def active_membership(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        membership = get_membership(request)

        if membership == 1:
            return function(request, *args, **kwargs)
        else:
            return redirect('join')

    return wrap