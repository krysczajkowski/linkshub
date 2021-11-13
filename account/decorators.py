from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import BannedUser

def check_ban(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            user = BannedUser.objects.get(user=request.user)
            return HttpResponseRedirect('/you_are_banned/')
        except BannedUser.DoesNotExist:
            return function(request, *args, **kwargs)


    return wrap