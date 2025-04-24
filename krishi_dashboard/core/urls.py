from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-form/', register_view, name='register_form'),
    path('', login_view, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-data/', manage_data, name='manage_data'),
    path('add-project/', views.add_project, name='add_project'),
]
