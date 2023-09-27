from django.contrib import admin

from picture.models import Image, ExpiringLink


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(ExpiringLink)
class ExpiringLink(admin.ModelAdmin):
    list_display = ('id', 'expiration_time')

