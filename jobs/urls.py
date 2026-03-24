from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('job/create/', views.create_job, name='create_job'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
