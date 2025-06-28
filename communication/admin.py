from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'date_sent', 'is_read')
    list_filter = ('is_read', 'date_sent')
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username') 