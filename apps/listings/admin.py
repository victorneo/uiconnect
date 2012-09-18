from django.contrib import admin
from .models import Listing, ListingImage, Collection


class ListingAdmin(admin.ModelAdmin):
    exclude = ('likes',)


class ListingImageAdmin(admin.ModelAdmin):
    pass


class CollectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingImage, ListingImageAdmin)
admin.site.register(Collection, CollectionAdmin)
