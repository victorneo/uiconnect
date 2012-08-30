from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm


def login(request):
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
