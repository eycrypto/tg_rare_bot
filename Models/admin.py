from django.contrib import admin

from Models.models import Message, API, System, Rare


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(API)
class APIAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'phone']


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    pass


@admin.register(Rare)
class RareAdmin(admin.ModelAdmin):
    pass

@admin.register(SendMessage)
class SendMessageAdmin(admin.ModelAdmin):
    pass
