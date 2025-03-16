from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Profile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number']

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        groups = validated_data.pop('groups', None)  # ✅ Remove `groups` before passing data
        user_permissions = validated_data.pop('user_permissions', None)  # ✅ Remove `user_permissions`

        user = CustomUser.objects.create_user(**validated_data)  # ✅ Pass cleaned data

        if groups:
            user.groups.set(groups)  # ✅ Set `groups` safely
        if user_permissions:
            user.user_permissions.set(user_permissions)  # ✅ Set `user_permissions` safely

        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'profile_picture']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
