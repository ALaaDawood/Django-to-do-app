from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from user.forms import LoginForm, RegisterForm, User


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("todo/dashboard/")
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
                return redirect("todo/dashboard/")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})
