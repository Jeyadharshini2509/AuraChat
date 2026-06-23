from django.contrib import admin

from .models import ChatThread, Message


@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at")
    list_filter = ("user",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("thread", "role", "short_content", "created_at")
    list_filter = ("role",)

    def short_content(self, obj):
        return obj.content[:60]
