from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.models import Group
from user.forms import LoginForm, RegisterForm, User


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name="normal_user"))
            auth_login(request, user)
            return redirect("/todolist/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data["email"])
            except User.DoesNotExist:
                return HttpResponse("user not found")
            if user.check_password(form.cleaned_data["password"]):
                auth_login(request, user)
                return redirect("/todolist/")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("/user/login?next=/")
