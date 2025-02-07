from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from .models import CustomUser, Profile
from django.contrib.auth.mixins import LoginRequiredMixin

class RegistrationView(CreateView):
    model = CustomUser
    from_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy ('login')

    def form_valid(self, form):        
        user= form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def get_form_class(self):
        return CustomUserCreationForm
    

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'registration/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')  
    

class HomeView(TemplateView, LoginRequiredMixin):
    template_name = 'registration/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user 

        if user.is_authenticated:
            context['profile']= user.profile
        else:
            context['profile']= None
        return context 

class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "registration/user_update.html"  
    success_url = reverse_lazy('home') 

    def get_object(self, queryset=None):
        return self.request.user

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "registration/profile_update.html"
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        # Check if the request method is POST
        if self.request.method == 'POST':
            profile = form.save()
            user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
            if user_form.is_valid():
                user_form.save()

            return redirect(self.success_url)
        else:
            # You can return some other response here if it's not a POST request
            return super().form_invalid(form)
# Create your views here.
