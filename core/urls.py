from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),

    
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    
    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('hr/interviews/', views.hr_interviews, name='hr_interviews'),
    path('hr/applications/', views.hr_applications, name='hr_applications'),

    path(
        'hr/application/<int:session_id>/<str:status>/',
        views.update_application_status,
        name='update_application_status'
    ),

    
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('interview/start/<int:interview_id>/', views.start_interview, name='start_interview'),
]
