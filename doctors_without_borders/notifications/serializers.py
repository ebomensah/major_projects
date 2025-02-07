from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'read_status', 'timestamp']
        read_only_fields = ['id', 'message', 'timestamp'] 