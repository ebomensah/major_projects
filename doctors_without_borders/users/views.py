from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CustomUser, Profile, PatientHistory
from .serializers import CustomUserSerializer, ProfileSerializer, UserUpdateSerializer, LoginSerializer, CustomUserRegistrationSerializer
from django.views.generic import TemplateView, View, UpdateView
from django.http import JsonResponse, HttpResponse
from rest_framework import serializers 
from django.contrib.auth.views import LogoutView, LoginView
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, DoctorOnboardingForm, PatientOnboardingForm, PharmacistOnboardingForm
from django.views import View
from rest_framework.views import APIView
from django.shortcuts import render
from django.views.generic.edit import CreateView


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'
    form_class = PasswordResetForm  # Default Django form for password reset

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


def user_is_doctor(user):
    return user.role == 'doctor'

def user_is_patient(user):
    return user.role == 'patient'

def user_is_pharmacist(user):
    return user.role == 'pharmacist'

def user_is_admin(user):
    return user.role == 'admin'


class CustomLoginView(LoginView):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "login.html", {"error": "Invalid credentials"})
        

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class OnboardingView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        
        if not hasattr(user, 'gender') or not hasattr(user, 'age'):
            return redirect('home')

        form = None  # Initialize form
        gender = user.gender
        age = user.age  

        if user.role == 'doctor':
            form = DoctorOnboardingForm()
        elif user.role == 'patient':
            form = PatientOnboardingForm()
        elif user.role == 'pharmacist':
            form = PharmacistOnboardingForm()
        else:
            return redirect('home')
        
        show_prostate_screening = gender == 'M' and age > 40
        show_cervical_screening = gender == 'F'
        show_breast_screening = gender == 'F'

        print(f"Gender: {gender}, Age: {age}, Show Prostate: {show_prostate_screening}, Show Cervical: {show_cervical_screening}, Show Breast: {show_breast_screening}")

        return render(request, 'registration/onboarding.html', {
            'form': form,
            'show_prostate_screening': show_prostate_screening,
            'show_cervical_screening': show_cervical_screening,
            'show_breast_screening': show_breast_screening
        })
    
    @method_decorator(login_required)
    def post(self, request):
        user = request.user

        if not hasattr(user, 'gender') or not hasattr(user, 'age'):
            return redirect('home')  # Redirect 

        # Determine the correct form based on the user's role
        if user.role == 'doctor':
            form = DoctorOnboardingForm(request.POST)
        elif user.role == 'patient':
            form = PatientOnboardingForm(request.POST)
        elif user.role == 'pharmacist':
            form = PharmacistOnboardingForm(request.POST)
        else:
            return redirect('home')

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
        
            # If the user is a patient, check and save to PatientHistory
            if user.role == 'patient':
                patient_history, created = PatientHistory.objects.get_or_create(user=user)
                profile.user = user  # Attach the user to the profile if not done already
                profile.save()  # Save PatientHistory

            # Redirect based on role
            return self.get_success_url(user)

        # If the form is invalid, re-render the form with existing data
        return render(request, 'registration/onboarding.html', {
            'form': form,
            'show_prostate_screening': request.POST.get('gender') == 'M' and int(request.POST.get('age', user.age)) > 40,
            'show_cervical_screening': request.POST.get('gender') == 'F',
            'show_breast_screening': request.POST.get('gender') == 'F'
        })
    
    def get_success_url(self, user):
        """Return the URL to redirect user to their respective dashboard after onboarding."""
        if user.role == 'doctor':
            return reverse_lazy('doctor_dashboard')
        elif user.role == 'patient':
            return reverse_lazy('patient_dashboard')
        elif user.role == 'pharmacist':
            return reverse_lazy('pharmacist_dashboard')
        elif user.role == 'admin':
            return reverse_lazy('admin_dashboard')
        
        return reverse_lazy('default_dashboard')  # Ensure all paths return a URL

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user= request.user
        role= user.role

        return render(request, "registration/dashboard.html", {"role": role})


class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/doctor_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not user_is_doctor(request.user) or not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, args, **kwargs)
        
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'registration/user_update.html'

    def get_object(self):
        return self.request.user  

    def form_valid(self, form):
        form.save()

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

    
class CustomRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('onboarding')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        login(self.request, user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('onboarding')
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('onboarding')  # Redirect to onboarding if already logged in
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context


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

from rest_framework.parsers import MultiPartParser, FormParser


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
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
                    {"message": "Login successful", "redirect_url": '/dashboard/'}, status=status.HTTP_200_OK
                )
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            "message": "Logout successful",
            "redirect_url": "/login"
            }, status=status.HTTP_200_OK)
    
class HomeView(TemplateView):
    template_name = 'registration/home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)






