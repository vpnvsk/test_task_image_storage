from django.contrib import admin

from .models import Tier, User, Thumbnail


@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ('id', 'size')


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'tier')