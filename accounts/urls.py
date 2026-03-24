from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('seekers/', views.seekers_list, name='seekers_list'),
    path('recruiters/', views.recruiters_list, name='recruiters_list'),
]
