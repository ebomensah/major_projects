from django.contrib import admin
from .models import CustomUser, Profile, DoctorHistory, PatientHistory, PharmacistHistory
from django.utils.html import format_html

class CustomUserAdmin (admin.ModelAdmin):
    list_display = ['title', 'first_name', 'last_name', 'age', 'role', 'profile_picture']
    search_fields = ['title', 'first_name', 'last_name', 'age', 'role']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.is_active = True
        super().save_model(request, obj, form, change)
admin.site.register (CustomUser, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user']
admin.site.register (Profile, ProfileAdmin)

class DoctorHistoryAdmin(admin.ModelAdmin):
    list_display = ['license_id', 'address', 'place_of_work', 'payment_options', 'payment_name']
    search_fields = ['license_id', 'address', 'place_of_work', 'payment_options', 'payment_name']
admin.site.register (DoctorHistory, DoctorHistoryAdmin)

class PatientHistoryAdmin(admin.ModelAdmin):
    list_fields = ['allergies', 'allergies_detail', 'chronic_disease_status', 'chronic_disease_detail', 'smoking_status', 'smoking_detail', 'alcohol_status', 'alcohol_detail', 'blood_group', 'genotype', 'implant', 'vitals', 'recent_labs', 'prostate_screening', 'cervical_cancer_screening']
    search_fields = ['allergies', 'allergies_detail', 'chronic_disease_status', 'chronic_disease_detail', 'smoking_status', 'smoking_detail', 'alcohol_status', 'alcohol_detail', 'blood_group', 'genotype', 'implant', 'vitals', 'recent_labs', 'prostate_screening', 'cervical_cancer_screening' ]
admin.site.register (PatientHistory, PatientHistoryAdmin)

class PharmacistHistoryAdmin(admin.ModelAdmin):
    list_fields= ['license_id', 'address_of_pharmacy', 'place_of_work', 'payment_options', 'payment_name']
    search_fields = ['license_id', 'address_of_pharmacy', 'place_of_work', 'payment_options', 'payment_name']
admin.site.register (PharmacistHistory, PharmacistHistoryAdmin)

