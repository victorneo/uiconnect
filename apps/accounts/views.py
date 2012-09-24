import binascii
import json
import os
import urlparse
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as lgin, logout as lgout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
import facebook
import requests
from .forms import *
from .models import UserProfile


def login(request):
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))

    form = LoginForm(request.POST or None)

    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        url = request.GET.get('next', reverse('dashboard'))

        if user:
            lgin(request, user)
            return redirect(url)
        else:
            messages.error(request, u'Invalid login.')

    server_url = 'http://%s/' % Site.objects.get(id=1).domain

    return render(request, 'accounts/login.html', {
        'form': form,
        'server_url': server_url,
    })


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


@login_required
def follow(request, user_id):
    data = {'success': True}
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        data['success'] = False
    else:
        if user != request.user:
            profile = user.get_profile()
            if profile in request.user.get_profile().following.all():
                profile.followers.remove(request.user.get_profile())
            else:
                profile.followers.add(request.user.get_profile())

            profile.save()
        else:
            data['success'] = False

    return HttpResponse(json.JSONEncoder().encode(data),
                        content_type='application/json')


@login_required
def following(request):
    following_users = request.user.get_profile().following.all()

    return render(request, 'accounts/following.html', {
        'following_users': following_users,
    })


@login_required
def unfollow(request, user_id):
    try:
        profile = User.objects.get(id=user_id).get_profile()
    except User.DoesNotExist:
        pass
    else:
        request.user.get_profile().following.remove(profile)
        request.user.get_profile().save()

    return redirect(reverse('accounts:following'))


def facebook_login(request):
    if request.user.is_authenticated() or \
            request.GET.get('code', None) is None:
        return redirect(reverse('index'))

    code = request.GET['code']

    server_url = 'http://%s/' % Site.objects.get(id=1).domain
    response = requests.get('https://graph.facebook.com/oauth/access_token?client_id=536337693059624&redirect_uri=%saccounts/facebook-login&client_secret=c933b8b99034657f9365b64031acc640&code=%s' % (server_url, code))

    # get access token
    access_token = urlparse.parse_qs(response.text)['access_token'][0]
    graph = facebook.GraphAPI(access_token)
    user_info = graph.get_object('me')
    fb_id = user_info['id']

    try:
        user = UserProfile.objects.get(fb_id=fb_id).user
    except UserProfile.DoesNotExist:
        user = User.objects.create_user(username=fb_id,
                                       password='',
                                       email=user_info['email'])
        user.first_name = user_info['name']
        user.save()
        user.get_profile().fb_id = fb_id
        user.get_profile().save()

    user = authenticate(fb_id=fb_id)
    lgin(request, user)

    return redirect(reverse('dashboard'))
