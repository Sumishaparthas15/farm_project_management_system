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
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.utils import timezone
from datetime import datetime
from datetime import date, timedelta
import calendar
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout


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
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or 'home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

class LoggedInUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'full_name': user.get_full_name(),
            'role': getattr(user, 'role', 'N/A')
        })
User = get_user_model()
@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')  # Get the email
        password = request.data.get('password')  # Get the password

        if not email or not password:
            return Response({'detail': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)  # Find user by email
            if user.check_password(password):  # Validate password
                token, created = Token.objects.get_or_create(user=user)  # Generate or fetch token
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data  # Return user data
                })
            else:
                return Response({'non_field_errors': ['Invalid password']}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'non_field_errors': ['Invalid email address']}, status=status.HTTP_400_BAD_REQUEST)
class LoggedInUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'full_name': user.get_full_name(),
            'role': getattr(user, 'role', 'N/A')
        })

def dashboard(request):
    total_farms = Farm.objects.count()
    total_fields = Field.objects.count()
    total_crops = Crop.objects.count()
    total_active_projects = Project.objects.exclude(status='Completed').count()

    status_counts = Project.objects.values('status').annotate(count=Count('id'))
    upcoming_projects = Project.objects.filter(deadline__gte=timezone.now()).order_by('deadline')

    # Calendar-related context
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)
    first_day = first_day_of_month.weekday()  # 0 = Monday, 6 = Sunday (ISO-8601)
    days_in_month = (date(today.year, today.month + 1, 1) - first_day_of_month).days
    
    # Create a list of days in the month
    days_in_month_list = list(range(1, days_in_month + 1))

    # Determine the empty cells before the first day of the month
    empty_cells_before_first_day = list(range(first_day))

    context = {
        'total_farms': total_farms,
        'total_fields': total_fields,
        'total_crops': total_crops,
        'total_active_projects': total_active_projects,
        'status_counts': status_counts,
        'upcoming_projects': upcoming_projects,  # Ensure this is passed
        'first_day': first_day,
        'days_in_month': days_in_month,
        'days_in_month_list': days_in_month_list,  # Pass the list to the template
        'empty_cells_before_first_day': empty_cells_before_first_day,  # Pass the empty cells
    }

    return render(request, 'dashboard.html', context)
def get_calendar_data(request):
    today = date.today()
    year = today.year
    month = today.month
    first_day_of_month = date(year, month, 1)
    _, num_days_in_month = calendar.monthrange(year, month)

    days_in_month_list = [first_day_of_month + timedelta(days=i) for i in range(num_days_in_month)]

    upcoming_projects = Project.objects.filter(deadline__year=year, deadline__month=month)

    return render(request, 'your_template.html', {
        'days_in_month_list': days_in_month_list,
        'upcoming_projects': upcoming_projects,
        'today': today,
        'empty_cells_before_first_day': range(first_day_of_month.weekday())
    })



def calendar_view(request):
    # Get today's date and the upcoming projects within the current month
    today = datetime.today()
    
    # Get the current month and year
    month = today.month
    year = today.year
    
    # Get the first day of the month and the total number of days in the month
    first_day, days_in_month = calendar.monthrange(year, month)
    
    # Generate a list of empty cells before the first day
    empty_cells_before_first_day = list(range(first_day))

    # Find the nearest deadline
    context = {
        'today': today,
        'first_day': first_day,
        'days_in_month': days_in_month,
        'empty_cells_before_first_day': empty_cells_before_first_day,
        # Pass other context values like projects here if needed
    }

    return render(request, 'dashboard.html', context)

User = get_user_model()
def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('home')  
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
def project(request):
    farms = Farm.objects.all()
    fields = Field.objects.all()
    users = CustomUser.objects.filter(role='field_worker')
    projects = Project.objects.exclude(status='Completed')



    return render(request, 'add_project.html', {
        'farms': farms,
        'fields': fields,
        'users': users,
        'projects': projects,   
    })
def work_project(request):
    projects = Project.objects.exclude(status='Completed')
    return render(request, 'work_dashboard.html', {
        
        'projects': projects,   
    })
def update_project_status(request, project_id):
    if not request.user.is_authenticated:
        # Handle unauthenticated user (redirect or return an error)
        return JsonResponse({'success': False, 'error': 'User is not authenticated'}, status=401)

    if request.method == "POST":
        # Ensure the logged-in user is the assigned user for the project
        project = get_object_or_404(Project, id=project_id, assigned_to=request.user)
        
        # Get the new status from the form data
        new_status = request.POST.get('status')
        
        # Validate if the new status is a valid choice
        if new_status in ['Pending', 'In Progress', 'Completed']:
            project.status = new_status
            project.save()
            return JsonResponse({'success': True, 'new_status': new_status})
        
        return JsonResponse({'success': False, 'error': 'Invalid status value'}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def add_project(request):
    
    farms = Farm.objects.all()
    fields = Field.objects.all()
    users = CustomUser.objects.exclude(role='Admin')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        farm_id = request.POST.get('farm_id')
        field_id = request.POST.get('field_id')
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status')

        # Check required fields
        if not all([title, description, deadline, assigned_to_id, status]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'add_project.html', {
                'farms': farms,
                'fields': fields,
                'users': users
            })

        try:
            assigned_to_user = CustomUser.objects.get(id=int(assigned_to_id))
        except (CustomUser.DoesNotExist, ValueError):
            messages.error(request, 'Assigned user is invalid.')
            return render(request, 'add_project.html', {
                'farms': farms,
                'fields': fields,
                'users': users
            })

        try:
            farm = Farm.objects.get(id=int(farm_id)) if farm_id else None
        except (Farm.DoesNotExist, ValueError):
            farm = None

        try:
            field = Field.objects.get(id=int(field_id)) if field_id else None
        except (Field.DoesNotExist, ValueError):
            field = None

        # Create the project
        Project.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            assigned_farm=farm,
            assigned_field=field,
            assigned_to=assigned_to_user,
            status=status
        )

        messages.success(request, 'Project added successfully.')
        return redirect('add_project')

    return render(request, 'add_project.html', {
        'farms': farms,
        'fields': fields,
        'users': users
    })