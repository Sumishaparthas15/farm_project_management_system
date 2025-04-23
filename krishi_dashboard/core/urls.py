from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-form/', register_view, name='register_form'),
    path('', login_view, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
