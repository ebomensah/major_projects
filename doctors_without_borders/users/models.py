from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField 

class CustomUser(AbstractUser):
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs.', 'Mrs'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
    ]
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True)
    ROLE_CHOICES = [
            ('patient', 'Patient'),
            ('doctor', 'Doctor'),
            ('admin', 'Admin'),
    ]
    role = models.CharField (max_length= 50, choices = ROLE_CHOICES, default= 'patient')
    age = models.PositiveIntegerField(default = '18')
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    
   
    
    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}" 

class Profile (models.Model):
    profile_picture = models.ImageField(upload_to= 'profile_pics/', default= 'default.jpg', blank= True, null=True)
    bio = models.TextField(blank=True, null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"



# Create your models here.
