from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reward


@login_required
def index(request):
    rewards = Reward.objects.all()
    template = 'rewards/index.html'

    if not request.user.is_authenticated:
        template = 'rewards/public.html'

    return render(request, template, {
        'rewards': rewards,
    })


@login_required
def redeem(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id)
    profile = request.user.get_profile()

    try:
        reward.redeem(profile)
    except Exception as e:
        raise e
        messages.error(request, u'Insufficient points to redeem.')
    else:
        messages.success(request, u'Redeemed! You should receive an email shortly with the discount code.')

    return redirect(reverse('rewards:index'))
