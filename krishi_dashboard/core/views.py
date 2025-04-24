from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def register_view(request):
    return render(request, 'register.html')

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def login_view(request):
    return render(request, 'login.html')


User = get_user_model()
@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')  # Get the email
        password = request.data.get('password')  # Get the password

        try:
            user = User.objects.get(email=email)  # Find user by email
            if user.check_password(password):  # Validate password
                token, created = Token.objects.get_or_create(user=user)  # Generate or fetch token
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data  # Return user data
                })
            else:
                return Response({'non_field_errors': ['Invalid password']}, status=400)
        except User.DoesNotExist:
            return Response({'non_field_errors': ['Invalid email address']}, status=400)
        

def dashboard(request):
    total_farms = Farm.objects.count()
    total_fields = Field.objects.count()
    total_crops = Crop.objects.count()
    total_active_projects = Project.objects.exclude(status='Completed').count()
    
    context = {
        'total_farms': total_farms,
        'total_fields': total_fields,
        'total_crops': total_crops,
        'total_active_projects': total_active_projects,
    }
    return render(request, 'dashboard.html', context)

User = get_user_model()

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # change to your actual dashboard view
        else:
            messages.error(request, 'Invalid credentials or not authorized.')

    return render(request, 'admin_login.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')  
def manage_data(request):
    farms = Farm.objects.all()
    fields = Field.objects.select_related('farm').all()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'farm':
            name = request.POST.get('name')
            if name:
                Farm.objects.create(name=name)
                messages.success(request, 'Farm added.')
                return redirect('manage_data')

        elif form_type == 'field':
            farm_id = request.POST.get('farm_id')
            name = request.POST.get('name')
            farm = Farm.objects.get(id=farm_id)
            Field.objects.create(farm=farm, name=name)
            messages.success(request, 'Field added.')
            return redirect('manage_data')

        elif form_type == 'crop':
            field_id = request.POST.get('field_id')
            name = request.POST.get('name')
            harvest_date = request.POST.get('harvest_date')
            field = Field.objects.get(id=field_id)
            Crop.objects.create(field=field, name=name, harvest_date=harvest_date)
            messages.success(request, 'Crop added.')
            return redirect('manage_data')

    return render(request, 'admin_dashboard.html', {'farms': farms, 'fields': fields})

def add_project(request):
    farms = Farm.objects.all()
    fields = Field.objects.all()
    users = CustomUser.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        farm_id = request.POST.get('farm_id')
        field_id = request.POST.get('field_id')
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status')

        project = Project.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            assigned_farm=Farm.objects.get(id=farm_id) if farm_id else None,
            assigned_field=Field.objects.get(id=field_id) if field_id else None,
            assigned_to=CustomUser.objects.get(id=assigned_to_id),
            status=status
        )
        messages.success(request, 'Project added successfully.')
        return redirect('add_project')
    return render(request, 'add_project.html', {'farms': farms, 'fields': fields, 'users': users})
