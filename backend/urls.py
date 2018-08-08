from django.contrib import admin
from django.urls import path, re_path
from backend import views

urlpatterns = [
    re_path('^curd.html$', views.curd),
    re_path('^curd_json.html$', views.curd_json)
]