from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, RegisterView, LoginView, LogoutView
from .views import CustomUserViewSet, HomeView, csrf_token_view
from .views import CustomLoginView, CustomLogoutView, CustomRegisterView, ProfileUpdateView


router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')


urlpatterns = [
    path('api/', include(router.urls)),
    # path("register/", RegisterView.as_view(), name="register"),
    # # path("api/login/", LoginView.as_view(), name="login"),
    # path("api/logout/", LogoutView.as_view(), name="logout"),
    path('', HomeView.as_view(), name='home'),
    # path('api/csrf/', csrf_token_view, name="csrf_token"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('api/auth/logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
]
