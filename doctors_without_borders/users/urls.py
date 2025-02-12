from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, RegisterView, LoginView, LogoutView
from .views import CustomUserViewSet, HomeView, csrf_token_view


router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('home/', HomeView.as_view(), name='home'),
    path('csrf/', csrf_token_view, name="csrf_token"),
]
