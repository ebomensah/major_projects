from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, HomeView, ProfileUpdateView, UserUpdateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profileupdate/',ProfileUpdateView.as_view(), name='update_profile'),
    path('userupdate/',UserUpdateView.as_view(), name='update_user'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]