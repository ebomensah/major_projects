from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, RegisterView, LoginView, LogoutView
from .views import CustomUserViewSet, HomeView, OnboardingView
from .views import CustomLoginView, CustomLogoutView, CustomRegisterView, UserUpdateView
from .views import DoctorDashboardView, PatientDashboardView, PharmacistDashboardView, AdminDashboardView, DefaultDashboardView
from .views import CustomPasswordResetView, password_reset_done, CustomPasswordResetConfirmView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')


urlpatterns = [
    path('api/', include(router.urls)),
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile_update'),
    path('doctor_dashboard/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('patient_dashboard/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('pharmacist_dashboard/', PharmacistDashboardView.as_view(), name='pharmacist_dashboard'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('default_dashboard/', DefaultDashboardView.as_view(), name='default_dashboard'),
    path('onboarding/', OnboardingView.as_view(), name='onboarding'),
    path('reset-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
