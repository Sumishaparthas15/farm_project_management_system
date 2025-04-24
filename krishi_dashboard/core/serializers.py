from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role']  

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])


    class Meta:
        model = CustomUser
        fields = ('email','username','role','password',)    

    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            email = validated_data['email'],username= validated_data['username'],
            role = validated_data['role'],password=validated_data['password']) 
        return user     