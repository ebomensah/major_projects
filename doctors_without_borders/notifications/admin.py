from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'message', 'read_status', 'timestamp')
    list_filter = ('read_status', 'timestamp')

# Register your models here.
