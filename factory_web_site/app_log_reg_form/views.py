from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import *

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("main:home_page"))
    else:
        form = SignUpForm()
    return render(request, "register-form.html", {'form': form, 'title': "Регистрация"})


def sign_in(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(reverse("main:home_page"))
            else:
                form.add_error("password", "Неверный пароль")
    else:
        form = SignInForm()
    return render(request, "login-form.html", {'form': form, 'title': "Вход в аккаунт"})

def log_out(request):
    logout(request)
    return redirect(reverse("main:home_page"))
