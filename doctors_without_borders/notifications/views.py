from django.shortcuts import render
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(read_status = True)

    @action (detail=True, methods = ['PATCH'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read_status = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status = status.HTTP_200_OK)
# Create your views here.
