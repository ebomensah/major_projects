from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, RegisterView, LoginView, LogoutView
from .views import CustomUserViewSet, HomeView
from .views import CustomLoginView, CustomLogoutView, CustomRegisterView, ProfileUpdateView
from .views import DoctorDashboardView, PatientDashboardView, PharmacistDashboardView, AdminDashboardView, DefaultDashboardView
from django.contrib.auth.views import LogoutView


router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')


urlpatterns = [
    path('api/', include(router.urls)),
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('doctor_dashboard/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('patient_dashboard/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('pharmacist_dashboard/', PharmacistDashboardView.as_view(), name='pharmacist_dashboard'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('default_dashboard/', DefaultDashboardView.as_view(), name='default_dashboard'),

]
