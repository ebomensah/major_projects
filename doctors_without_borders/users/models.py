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
            ('pharmacist', 'Pharmacist'),
    ]
    role = models.CharField (max_length= 50, choices = ROLE_CHOICES, default= 'patient')
    age = models.PositiveIntegerField(default = '18')
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to= 'profile_pics/', default='profile_pics/default.png', blank= True, null=True)
    first_time_login = models.BooleanField(default=True)

   
    
    
    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}" 

class Profile (models.Model):
    bio = models.TextField(blank=True, null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    recent_labs = models.ImageField(
        upload_to='lab_images/',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"


class PatientHistory(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="patient_history")
    allergies = models.CharField(max_length=255, blank=True, null=True)
    allergies_detail = models.TextField(blank=True, null=True)
    chronic_disease_status = models.CharField(max_length=50, blank=True, null=True)
    chronic_disease_detail = models.TextField(blank=True, null=True)
    smoking_status = models.CharField(max_length=50, blank=True, null=True)
    smoking_detail = models.TextField(blank=True, null=True)
    alcohol_status = models.CharField(max_length=50, blank=True, null=True)
    alcohol_detail = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    genotype = models.CharField(max_length=10, blank=True, null=True)
    implant = models.TextField(blank=True, null=True)
    vitals = models.TextField(blank=True, null=True)
    prostate_screening = models.CharField(max_length=10, blank=True, null=True)
    cervical_cancer_screening = models.CharField(max_length=10, blank=True, null=True)
    breast_cancer_screening = models.CharField(max_length=50, blank=True, null=True)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=50, blank=False)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Patient History"
    
class DoctorHistory(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="doctor_history")
    license_id = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    place_of_work = models.CharField(max_length=255)
    
    SPECIALIZATION_CHOICE = [
        ('Specialist', 'Specialist'),
        ('Medical Officer', 'MO'),
        ('Consultant', 'Consultant'),
    ]
    specialized = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICE, blank=True, null=True)
    
    PAYMENT_CHOICES = [
        ('mobile money', 'Mobile Money'),
        ('bank transfer', 'Bank Transfer'),
        ('paypal', 'Paypal'),
    ]
    payment_options = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    payment_name = models.CharField(max_length=255, help_text="Registered name on the preferred payment method")

    def __str__(self):
        return f"Doctor History - Dr. {self.user.first_name} {self.user.last_name}"
    
class PharmacistHistory(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="pharmacist_history")
    license_id = models.CharField(max_length=255, unique=True)
    address_of_pharmacy = models.CharField(max_length=255)
    place_of_work = models.CharField(max_length=255)

    PAYMENT_CHOICES = [
        ('mobile money', 'Mobile Money'),
        ('bank transfer', 'Bank Transfer'),
        ('paypal', 'Paypal'),
    ]
    payment_options = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    
    payment_name = models.CharField(max_length=255, help_text="Registered name on the preferred payment method")

    DELIVERY_OPTIONS = [
        ('Pick up only', 'Pick up only'),
        ('Delivery available', 'Delivery available'),
    ]
    delivery_options = models.CharField(max_length=50, choices=DELIVERY_OPTIONS)

    def __str__(self):
        return f"Pharmacist History - Dr. {self.user.first_name} {self.user.last_name}"