from django.contrib import admin
from .models import Reward


class RewardAdmin(admin.ModelAdmin):
    exclude = ('redeemed_by',)


admin.site.register(Reward, RewardAdmin)
