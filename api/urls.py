from django.urls import path, re_path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
# 这是一个路由映射，比如现在是在api项目下，那么下面匹配到的就是
# 127.0.0.1/api/users/, 调用后面的视图函数或者叫cbv
router.register(r'servers', views.ServerViewSet)

urlpatterns = [
    re_path('asset.html$', views.asset),
    re_path('server.html$', views.asset),
    path('', include(router.urls)),
]
