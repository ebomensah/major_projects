from django.urls import path, include
from .views import NotificationViewSet, NotificationListView, NotificationDetailView, mark_notification_read
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns=[
    path('api/', include(router.urls)),
    path('notifications/', NotificationListView.as_view(), name="notifications-list"),
    path("notifications/<int:pk>/", NotificationDetailView.as_view(), name="notification-detail"),
     path('notifications/read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
]
    