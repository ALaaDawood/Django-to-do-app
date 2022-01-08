from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import TaskForm
from .models import Task
from django.conf import settings
from django.contrib.auth.decorators import (
    permission_required,
)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))
    tasks = Task.objects.all()
    return render(request, "dashboard.html", {"tasks": tasks})


def admin_user_check(user):
    return user.is_admin


@permission_required(["todo.change_task", "todo.add_task"], raise_exception=True)
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
