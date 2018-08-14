from django.contrib import admin
from django.urls import path, re_path
from backend import views

urlpatterns = [
    re_path('^curd.html$', views.curd),
    re_path('^curd_json.html$', views.curd_json),
    re_path('^asset.html$', views.asset),
    re_path('^asset_json.html$', views.asset_json),
    re_path('^idc.html$', views.idc),
    re_path('^idc_json.html$', views.idc_json),
    re_path('^chart.html$', views.chart),
]