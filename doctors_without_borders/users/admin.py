from django.contrib import admin
from .models import CustomUser, Profile
from django.utils.html import format_html

class CustomUserAdmin (admin.ModelAdmin):
    list_display = ['title', 'first_name', 'last_name', 'age', 'role']
    search_fields = ['title', 'first_name', 'last_name', 'age', 'role']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.is_active = True
        super().save_model(request, obj, form, change)
admin.site.register (CustomUser, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'profile_picture']
    search_fields = ['user']
admin.site.register (Profile, ProfileAdmin)

# Register your models here.
