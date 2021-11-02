from django.shortcuts import render, HttpResponse
from .models import Task
from rest_framework import status
from django.utils.functional import SimpleLazyObject
from django.conf import settings
from django.shortcuts import redirect

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    tasks = Task.objects.all()
    return render(request, 'dashboard.html', {"tasks": tasks})



def create(request):
    print(request.user)
    if isinstance(request.user,SimpleLazyObject):
        return HttpResponse({},status = status.HTTP_401_UNAUTHORIZED)

    return HttpResponse({})
