from django.contrib import admin
from .models import Listing, ListingImage


class ListingAdmin(admin.ModelAdmin):
    pass


class ListingImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingImage, ListingImageAdmin)
