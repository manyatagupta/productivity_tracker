from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.index, name='index'),
    path('register/', views.register, name='register'),
]