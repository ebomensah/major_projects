from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from appointments.views import AppointmentViewSet, ConsultationViewSet
from notifications.views import NotificationViewSet
from users.views import CustomUserViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointments')
router.register(r'consultations', ConsultationViewSet, basename='consultations')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include ('users.urls')),
    path('', include ('appointments.urls')),
    path('', include ('notifications.urls')),
    ] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
