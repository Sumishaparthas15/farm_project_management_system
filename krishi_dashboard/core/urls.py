from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-form/', register_view, name='register_form'),
    path('', login_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('api/user/', LoggedInUserView.as_view(), name='logged_in_user'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_calendar_data/', views.get_calendar_data, name='get_calendar_data'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('project/', views.project, name='project'),
    path('work_project/', views.work_project, name='work_project'),
   path('update-status/<int:project_id>/', views.update_project_status, name='update_project_status'),

    path('add-project/', views.add_project, name='add_project'),

    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-data/', manage_data, name='manage_data'),
    
]
