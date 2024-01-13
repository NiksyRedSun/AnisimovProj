from django.contrib import admin
from django.urls import path, re_path, register_converter
from . import views




urlpatterns = [
    path('', views.PrintSiteHome.as_view(), name="home"), #127.0.0.1:8000
]
