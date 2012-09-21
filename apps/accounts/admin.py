from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    exclude = ('following',)


admin.site.register(UserProfile, UserProfileAdmin)
