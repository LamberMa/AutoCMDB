restful 面向资源编程，没有它还是该怎么写代码就怎么写代码，restful就是这样定义了一个规则

把网络上的任何东西都当做是一个资源，资源应该是一个名词，比如order，而不应该是get_order
通过不同的方法来对资源做不同的操作：
GET：获取
POST：增加
PUT：修改
DELETE：删除

后端在返回的数据更规范的不仅仅是返回数据还应该返回一个状态码（status code）
比如：200（OK）、404（Not Found）、500（InternalServer Error）、403（Forbidden）

cmdb的操作中就是不借助任何框架，实现restful接口，自定义后台管理组件


# 不推荐使用的接口：django rest framework
install:
pip3 install djangorestframework

注册app，加入到settings

注册路由：
from rest_framework import routers
from . import views

router = router.DefaultRouter()
router.register(r'users', views.UserInfoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]


django rest framework请求流程：

1、url生成的本质
url(r'servers/$', views.ServeView)

基于cbv：
class ServerView(APIview):
    
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from . import models
from . import serializers

class UserList(APIView):
    def get(self, request, *args, **kwargs):
        user_list = models.UserInfo.objects.all()
        serializer = serializers.MySerialzer(instance=user_list, many=True)
        return Response(serializers.data)
        
    
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = serializers.MySerialzer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




注意事项：
1. 方法，put，get，delete，post，还有一个就是状态码。
2、url上得是名词，也就是资源得是名词。
3、版本号：比如xxx/api/v1/server.html，或者v1.oldbouedu.com这样的

django的restful框架：唯一的亮点就是界面的可视化，并且可以快速搭建api