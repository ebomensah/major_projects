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
from .models import CustomUser, Profile, PatientHistory, DoctorHistory, PharmacistHistory
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

        print(f"Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard if not first-time login
        return render(request, "login.html", {"error": "Invalid credentials"})
        

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class OnboardingView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user

        # Ensure user has necessary attributes
        if not hasattr(user, 'gender') or not hasattr(user, 'age'):
            return redirect('dashboard')

        # Select the correct form based on role
        form = None
        if user.role == 'doctor':
            form = DoctorOnboardingForm()
        elif user.role == 'pharmacist':
            form = PharmacistOnboardingForm()
        elif user.role == 'patient':
            form = PatientOnboardingForm()
        else:
            return redirect('dashboard')
        
        age= user.age
        gender= user.gender

        from django.forms import HiddenInput

        if form and isinstance(form, PatientOnboardingForm):
            # Check if fields exist in the form before attempting to hide
            if 'prostate_screening' in form.fields and not (gender == 'M' and age >= 40):
                form.fields['prostate_screening'].widget = HiddenInput()

            if 'cervical_cancer_screening' in form.fields and not (gender == 'F' and age >= 18):
                form.fields['cervical_cancer_screening'].widget = HiddenInput()
                form.fields['breast_cancer_screening'].widget = HiddenInput()

        return render(request, 'registration/onboarding.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        user = request.user

        if user.role == 'patient' and hasattr(user, 'patient_history'):
            return redirect('dashboard') 
        if user.role == 'doctor' and hasattr(user, 'doctor_history'):
            return redirect('dashboard') 
        if user.role == 'pharmacist' and hasattr(user, 'pharmacist_history'):
            return redirect('dashboard') 

        form= None
        if user.role == 'doctor':
            form = DoctorOnboardingForm(request.POST, request.FILES)
        elif user.role == 'pharmacist':
            form = PharmacistOnboardingForm(request.POST, request.FILES)
        elif user.role == 'patient':
            form = PatientOnboardingForm(request.POST, request.FILES)
        else:
            return redirect('dashboard')
        
        form.instance.user = user 

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()

            if user.role == 'patient' and not hasattr(user, 'patient_history'):
                PatientHistory.objects.create(user=user)  # Create the patient's history

            # Mark onboarding as completed
            if user.first_time_login:
                user.first_time_login = False
                user.save()
            
            return redirect ('dashboard')
        else:
            print("Form is NOT valid")
            print(form.errors)
            form.add_error(None, "There are errors in the form. Kindly correct them and resubmit.")
            return render(request, 'registration/onboarding.html', {'form': form})

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user= request.user
        role= user.role

        return render(request, "registration/dashboard.html", {"role": role})

        
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
        return reverse_lazy('dashboard')  # Redirect all users to the same dashboard
        

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
        user.is_active = True  # Ensure user is active by default
        user.first_time_login = True  # Ensure first-time login is marked as True
        user.save()

        login(self.request, user)
        return super().form_valid(form)
    
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






