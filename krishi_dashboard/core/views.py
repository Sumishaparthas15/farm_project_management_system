from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

def register_view(request):
    return render(request, 'register.html')

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

def login_view(request):
    return render(request, 'login.html')

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
 
def dashboard_view(request):
    return render(request, 'dashboard.html')
