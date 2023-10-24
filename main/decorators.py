from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib import messages

def only_mentors(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.role == 'Mentor':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have access to view this page!")
    return _wrapped_view