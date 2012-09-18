from django.shortcuts import render, redirect
from .models import Reward


def index(request):
    rewards = Reward.objects.all()

    return render(request, 'rewards/index.html', {
        'rewards': rewards,
    })
