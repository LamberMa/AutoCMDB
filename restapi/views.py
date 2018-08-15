import json
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core import serializers
from rest_framework import serializers as restserializers
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from repository import models
from restapi import serializers as myserializers


class ServerView(APIView):

    def get(self, request, *args, **kwargs):
        # 获取列表
        data_list = models.UserProfile.objects.all()
        # data = serializers.serialize('json', data_list)
        # 上面使用django的方式序列化的，使用restfulapi也支持序列化
        # 使用restfulapi的序列化需要自己写上一个序列化的工具，因此我这里新建了一个serializers.py文件
        # 对于restfulapi的序列化，不仅有序列化的功能还有form组件验证功能
        # many表示序列化的时候，为true表示是个列表。如果只是一个数据就不需要加many了。
        data = myserializers.MySer(instance=data_list, many=True)
        # 做get请求的时候无需做验证,data.data是一个orderedDict类型
        # 要想然用户看见，就需要json序列化一下
        # 因为HttpResponse只加字符串类型，如果加了个字典就只把key列出来了。
        # return HttpResponse(json.dumps(data.data))
        # 或者直接使用JsonResponse就可以了
        return JsonResponse(data.data, safe=False)

    def post(self, request, *args, **kwargs):
        # 创建数据，此时的request已经是一个封装后的request了。
        # 现在是rest_framework.request.Request的对象
        # from rest_framework.request import Request
        # 里面有一个self._request = request，实际上这个_request就是我们的原来的request
        # 其中request.data就是这个Request对象帮我们取到得值。不想这么用的话也可以
        # request._request.body去取数据。request.data相当于直接拿到数据变成字典类型了。
        # 增加数据无非就是调用model模型添加数据，在这里完全可以直接添加
        # 不过restful中还支持一种写法
        data = JSONParser().parse(request)
        # 提交instance的时候提交的是一个对象不用验证，当提交的是一个data的时候就要进行form组件验证了。
        serializer = myserializers.MySer(data=data)
        if serializer.is_valid():
            # serialzer.data 所有的数据
            # serialzer.error
            # serialzer.validated_data 验证成功的数据
            # 如果有instance，执行update方法，否则执行create方法
            serializer.save()
        return HttpResponse('...')


class ServerDetail(APIView):
    # 获取当前详细
    def get(self, request, nid):
        # 获取单挑数据
        pass

    def delete(self, request, nid):
        pass

    def put(self, request, nid):
        pass

