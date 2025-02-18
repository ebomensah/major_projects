from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CustomUser, Profile
from .serializers import CustomUserSerializer, ProfileSerializer, UserUpdateSerializer, LoginSerializer
from django.views.generic import TemplateView, View, UpdateView
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from rest_framework import serializers 
from django.contrib.auth.views import LogoutView, LoginView
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model


def user_is_doctor(user):
    return user.role == 'doctor'

def user_is_patient(user):
    return user.role == 'patient'

def user_is_pharmacist(user):
    return user.role == 'pharmacist'

def user_is_admin(user):
    return user.role == 'admin'


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        if user.role == 'doctor':
            return redirect(reverse_lazy('doctor_dashboard'))
        
        elif user.role == 'patient':
            return redirect(reverse_lazy('patient_dashboard'))
        
        elif user.role == 'pharmacist':
            return redirect(reverse_lazy('pharmacist_dashboard'))
        
        elif user.role == 'admin':
            return redirect(reverse_lazy('admin_dashboard'))

        return redirect('default_dashboard') 
    
    def form_invalid(self, form):
        """Show error messages if login fails"""
        messages.error(self.request, "Invalid username or password.")
        return self.render_to_response(self.get_context_data(form=form))
    


class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/doctor_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not user_is_doctor(request.user) or not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, args, **kwargs)
    

class DefaultDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/default_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not (user_is_admin(request.user) or user_is_doctor(request.user) or user_is_patient(request.user) or user_is_pharmacist(request.user)):
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class PatientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/patient_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not user_is_patient(request.user) or not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class PharmacistDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/pharmacist_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not user_is_pharmacist(request.user) or not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/admin_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not user_is_admin(request.user) or not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'registration/profile_update.html'

    def get_object(self):
        return self.request.user.profile  # Assuming a OneToOne relation with User

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)
        
    def get_success_url(self):    
        user = self.request.user
        if user.role == 'doctor':
            return reverse_lazy ('doctor_dashboard')
        elif user.role == 'patient':
            return reverse_lazy('patient_dashboard')
        elif user.role == 'pharmacist':
            return reverse_lazy('pharmacist_dashboard')
        elif user.role == 'admin':
            return reverse_lazy ('admin_dashboard')
        
        return reverse_lazy ('default_dashboard')
        

class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'redirect_url': reverse('login')})  # Adjust the redirect URL as needed

    


# @method_decorator(csrf_exempt, name='dispatch')
# class CustomLogoutView(LogoutView):
#     def dispatch(self, request, *args, **kwargs):
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if AJAX
#             self.logout(request)
#             return JsonResponse({"message": "Logged out"}, status=200)  # Return JSON for AJAX
#         return redirect ('login')

class CustomRegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'me']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        if Profile.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError({"error":"A profile already exists for this user."})
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return Response(
                    {"message": "Login successful"}, status=status.HTTP_200_OK
                )
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    
class HomeView(TemplateView):
    template_name = 'registration/home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)






