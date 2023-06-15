from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard, name= 'dashboard'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('image/delete/<str:id>', views.delete_image, name='delete'),
    
    path('', views.home, name='home'),
]
