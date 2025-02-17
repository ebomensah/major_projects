from django.shortcuts import render, get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import JsonResponse

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


class NotificationListView(ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)  # Filter by logged-in user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['notifications']:
            context['message'] = 'You have no notifications'  # Add a message if no notifications
        return context




def mark_notification_read(request, notification_id):
    # Ensure the notification belongs to the logged-in user
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()

    # Return a JSON response to indicate success
    return JsonResponse({"status": "success"})


class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = "notifications/notification_detail.html"
    context_object_name = "notification"

    def get_object(self):
        notification = super().get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return notification