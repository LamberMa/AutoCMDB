from django.contrib import admin
from django.urls import path, re_path
from api import views

urlpatterns = [
    re_path('asset.html$', views.asset),
]
