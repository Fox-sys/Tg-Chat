from django.contrib import admin

from . import models


class ChatInline(admin.StackedInline):
    model = models.Chat
    extra = 1


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'username')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'tg_username', 'banned')
    inlines = [ChatInline]
