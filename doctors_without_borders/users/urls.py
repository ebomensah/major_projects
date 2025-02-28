from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, RegisterAPIView, LoginView, LogoutView, CustomLogoutView
from .views import CustomUserViewSet, HomeView, OnboardingView
from .views import CustomLoginView, CustomLogoutView, CustomRegisterView, UserUpdateView
from .views import CustomPasswordResetView, password_reset_done, CustomPasswordResetConfirmView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import LoginAPIView, DashboardView


router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')


urlpatterns = [
    path('api/', include(router.urls)),
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(next_page='dashboard'), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='/login/'), name='logout'),
    path('api/login/', LoginAPIView.as_view(), name='login_api'),
    path('api/logout/', LogoutView.as_view(next_page='login'), name='api-logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('api/register/', RegisterAPIView.as_view(), name='register_api'),
    path('profile/', UserUpdateView.as_view(), name='profile_update'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('onboarding/', OnboardingView.as_view(), name='onboarding'),
    path('reset-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
