from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as lgin, logout as lgout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm


def login(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

        if user:
            lgin(request, user)
            return redirect(reverse('index'))
        else:
            messages.error(request, u'Invalid login.')

    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    lgout(request)
    return redirect(reverse('index'))


def register(request):
    form = RegistrationForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        try:
            user = User.objects.get(username=form.cleaned_data['username'])
        except User.DoesNotExist:
            user = None

        if user is None:
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email'],
            )
            user.bio = form.cleaned_data['bio']
            user.avatar = form.cleaned_data['avatar']
            user.save()

            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            lgin(request, user)
            return redirect(reverse('index'))
        else:
            messages.error(request, u'Username has been taken.')

    return render(request, 'accounts/register.html', {'form': form})
