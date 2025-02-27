from django import forms
from .models import CustomUser, Profile, PharmacistHistory, DoctorHistory, PatientHistory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['role','title', 'last_name', 'first_name', 'age', 'email', 'phone_number', 'profile_picture', 'username', 'password1', 'password2']

    def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if password1 and password2 != password2:
                raise forms.ValidationError("The two password fields must match.")
            return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class':'form-ocntrol'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


class DoctorOnboardingForm(forms.ModelForm):
    PAYMENT_CHOICES=[
        ('mobile money', 'Mobile Money'),
        ('bank transfer', 'Bank Transfer'),
        ('paypal', 'Paypal'),
    ]
    
    license_id = forms.CharField(max_length=255, label='Enter your License ID here', required=True)
    address = forms.CharField(max_length=255, required=True)
    place_of_work = forms.CharField(max_length=255)
    payment_options = forms.ChoiceField(choices=PAYMENT_CHOICES, label= 'What is your preferred payment method?', required=True)
    payment_name = forms.CharField(max_length=255, label='What is the registered name on the preferred payment method?', required=True)
    

    class Meta:
        model= DoctorHistory
        fields= ['license_id', 'address', 'place_of_work', 'payment_options', 'payment_name']


class PatientOnboardingForm(forms.ModelForm):
    BASE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Not applicable', 'N/A')
    ]
    CHRONIC_DISEASE_CHOICES= [
        ('Hypertension', 'Hypertension'),
        ('Diabetes', 'Diabetes'),
        ('Sickle Cell Disease', 'Sickle Cell disease'),
        ('Asthma', 'Asthma'),
        ('G6PD', 'G6PD'),
        ('Other', 'Other')
    ]
    GENOTYPE_CHOICES=[
        ('AA', 'AA'),
        ('AS', 'AS'),
        ('SS', 'SS'),
        ('SC', 'SC'),
        ('CC', 'CC'),
        ('UNKNOWN', 'Unknown'),
    ]
    BLOOD_GROUP_CHOICES=[
        ('O_POSITIVE', 'O+'),
        ('O_NEGATIVE', 'O-'),
        ('A_POSITIVE', 'A+'),
        ('A_NEGATIVE', 'A-'),
        ('B_POSITIVE', 'B+'),
        ('B_NEGATIVE', 'B-'),
        ('AB_POSITIVE', 'AB+'),
        ('AB_NEGATIVE', 'AB-'),
        ('UNKNOWN', 'Unknown'),
    ]


    age= forms.IntegerField(required=True, label='Age', widget=forms.HiddenInput())
    allergies = forms.ChoiceField(required=True, label='Do you have any allergies?', choices=BASE_CHOICES)
    allergies_detail = forms.CharField(max_length=255, label='List those allergies here', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    chronic_disease_status = forms.ChoiceField(required=True, choices=BASE_CHOICES, label='Do you have any chronic disease?')
    chronic_disease_detail = forms.MultipleChoiceField(required=False, choices=CHRONIC_DISEASE_CHOICES, label='Select any chronic diseases you have:', widget=forms.CheckboxSelectMultiple)
    smoking_status = forms.ChoiceField(required=True, choices=BASE_CHOICES, label='Do you smoke?')
    smoking_detail = forms.CharField(max_length=500, label='If yes, how often do you smoke and how many packs do you take in a day?')
    alcohol_status = forms.ChoiceField(choices=BASE_CHOICES, label='Do you take alcohol?')
    alcohol_detail= forms.CharField(max_length=500, label='If yes, How often do you take alcohol?')
    blood_group = forms.ChoiceField(required=True, label='What is your blood group?', choices=BLOOD_GROUP_CHOICES)
    genotype = forms.ChoiceField(required=True, label='What is your genotype?', choices=GENOTYPE_CHOICES)
    implant=forms.CharField(max_length=500, label='Do you have any form of implant? Kindly state that here:', required=True)
    vitals = forms.CharField(max_length=500, label='State the results of your last check for the following(Blood pressure, Pulse Rate, Random Blood Glucose)', required=True)
    recent_labs = forms.ImageField(required=False,
        label= 'Have you done any recent labs? Kindly upload the results here:')
    prostate_screening = forms.ChoiceField(label="Have you been screened for prostate disease?", choices=BASE_CHOICES, required=True)
    cervical_cancer_screening = forms.ChoiceField(label='Have you been screened for lesions of the cervix?', choices=BASE_CHOICES, required=True)
    breast_cancer_screening = forms.ChoiceField(label='Have you been screened for lesions of the breast?', choices=BASE_CHOICES, required=True)

    class Meta:
        model = PatientHistory
        # fields= ['allergies', 'allergies_detail', 'chronic_disease_status', 'chronic_disease_detail', 'smoking_status', 'smoking_detail', 'alcohol_status', 'alcohol_detail', 'blood_group', 'genotype', 'implant', 'vitals', 'recent_labs']
        fields= '__all__'
        exclude = ['user', 'gender']

    
    def save(self, commit=True):
        patient_history = super().save(commit=False)
        patient_history.user = self.instance.user  # Link history to user

        if commit:
            patient_history.save()
        return patient_history


class PharmacistOnboardingForm(forms.ModelForm):
    PAYMENT_CHOICES=[
        ('mobile money', 'Mobile Money'),
        ('bank transfer', 'Bank Transfer'),
        ('paypal', 'Paypal'),
    ]
    DELIVERY_OPTIONS = [
        ('Pick_up_only', 'Pick up only'),
        ('Delivery available', 'Delivery available')
    ]
    
    license_id = forms.CharField(max_length=255, required=True, label='Enter your License ID here')
    address_of_pharmacy = forms.CharField(max_length=255, required=True)
    place_of_work = forms.CharField(max_length=255, required=True)
    payment_options = forms.ChoiceField(choices=PAYMENT_CHOICES, label= 'What is your preferred payment method?', required=True)
    payment_name = forms.CharField(max_length=255, label='What is the registered name on the preferred payment method?', required=True)
    delivery_options = forms.ChoiceField(
    choices=DELIVERY_OPTIONS,
    label="What delivery options does your pharmacy offer?",
    required=True
)
    

    class Meta:
        model= PharmacistHistory
        fields= ['license_id', 'address_of_pharmacy', 'place_of_work', 'payment_options', 'payment_name']