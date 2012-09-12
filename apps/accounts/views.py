import os
import binascii
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as lgin, logout as lgout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *


def login(request):
    if request.user.is_authenticated():
        return reverse('dashboard')

    form = LoginForm(request.POST or None)

    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        url = request.GET.get('next', reverse('dashboard'))

        if user:
            lgin(request, user)
            return redirect(url)
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
            user.first_name = form.cleaned_data['name']
            user.save()

            user.get_profile().bio = form.cleaned_data['bio']
            user.get_profile().avatar = form.cleaned_data['avatar']
            user.get_profile().save()

            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            lgin(request, user)
            return redirect(reverse('index'))
        else:
            messages.error(request, u'Username has been taken.')

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    profile = user.get_profile()
    initial = {
        'name': user.first_name,
        'email': user.email,
        'bio': profile.bio,
        'avatar': profile.avatar,
    }
    form = ProfileForm(request.POST or None, request.FILES or None, initial=initial)

    if form.is_valid():
        user.first_name = form.cleaned_data['name']
        user.email = form.cleaned_data['email']

        if form.cleaned_data['password']:
            user.set_password(form.cleaned_data['password'])

        user.save()
        profile.bio = form.cleaned_data['bio']

        if form.cleaned_data.get('avatar', None):
            if profile.avatar and form.cleaned_data['avatar'] != profile.avatar:
                profile.avatar.delete()

            profile.avatar = form.cleaned_data['avatar']
        elif request.POST.get('avatar-clear', None) and profile.avatar:
            profile.avatar.delete()


        profile.save()

        messages.success(request, u'Your profile has been updated.')
        return redirect(reverse('accounts:profile'))

    return render(request, 'accounts/profile.html', {'form': form})


def forgot_password(request):
    form = ForgotPasswordForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        try:
            user = User.objects.get(username=form.cleaned_data['username'])
            password = binascii.b2a_hex(os.urandom(20))
            user.set_password(password)
            user.save()

            send_mail(
                'Your temporary password',
                '%s' % password,
                'uiconnect303@gmail.com',
                [user.email,]
            )

            messages.success(request, u'Email with temporary password has been sent.')
            return redirect(reverse('accounts:login'))

        except User.DoesNotExist:
            messages.error(request, u'Invalid username.')

    return render(request, 'accounts/forgot_password.html', {
        'form': form,
    })
