from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('core.urls')),

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('hr/', views.hr_dashboard, name='hr_dashboard'),
    path('candidate/', views.candidate_dashboard, name='candidate_dashboard'),

    path('hr/create-interview/', views.create_interview, name='create_interview'),
    path('hr/interviews/', views.hr_interviews, name='hr_interviews'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('register/', views.register, name='register'),

    path('hr/applications/', views.hr_applications, name='hr_applications'),

    path('interview/start/<int:interview_id>/', views.start_interview, name='start_interview'),

path(
        'hr/application/<int:session_id>/<str:status>/',
        views.update_application_status,
        name='update_application_status'
    ),

]
