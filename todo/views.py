from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, HttpResponse

from todo.forms import TaskForm
from .models import Task
from rest_framework import status
from django.utils.functional import SimpleLazyObject
from django.conf import settings
from django.shortcuts import redirect


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))
    tasks = Task.objects.all()
    return render(request, "dashboard.html", {"tasks": tasks})


def task_view(request, task_id=None):
    if task_id is None:
        task = Task()
    else:
        task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return HttpResponseRedirect(f"/todolist/{task.id}/")
    else:
        task_form = TaskForm(instance=task)
    return render(request, "task.html", {"form": task_form})


# def create(request):
#     print(request.user)
#     if isinstance(request.user, SimpleLazyObject):
#         return HttpResponse({}, status=status.HTTP_401_UNAUTHORIZED)

#     return HttpResponse({})
