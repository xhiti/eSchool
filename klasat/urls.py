from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.klasat, name='classes'),
    path('shto/', views.shto_klase, name='add-class'),
    path('fshi/<slug:pk>/', views.fshi_klase, name='delete-class'),
    path('modifiko/<slug:pk>/', views.modifiko_klase, name='edit-class'),
]
