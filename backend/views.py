import json
from datetime import datetime, date

from django.shortcuts import render, HttpResponse
from repository import models


# Create your views here.
def curd(request):

    return render(request, 'backend/curd.html')


def curd_json(request):
    # 注意这里还是可以跨表的，可以动态的放在用户的cookie里。
    table_config = [
        {
            'q': 'id',
            'title': 'ID',
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@id'},
            }
        },
        {
            'q': 'hostname',
            'title': '主机名',
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@hostname'},
            }
        },
        {
            'q': 'create_at',
            'title': '创建时间',
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@create_at'},
            }
        },
        {
            'q': 'asset__cabinet_num',
            'title': '机柜号',
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@asset__cabinet_num'},
            }
        },
        {
            'q': 'asset__business_unit__name',
            'title': '业务线名称',
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@asset__business_unit__name'},
            }
        },
        # 页面标题显示操作，操作为删除，编辑，应该是个a标签，这里的q不能随便写。
        # 我这可以写一个None，意味着不取，但是values_list要过滤
        # 因为values_list这个列表里不允许存在None。
        {
            'q': None,
            'title': '操作',
            'text': {
                'tpl': '<a href="/backend/del?nid={nid}">删除</a>',
                'kwargs': {'nid': '@id'},
            }
        },
    ]
    values_list = [row['q'] for row in table_config if row['q']]
    # for row in table_config:
    #     values_list.append(row['q'])
    # values_list = ['id', 'hostname']

    # v = models.Server.objects.all()
    # from django.core import serializers
    # serializers可以针对queryset对象进行序列化。
    # data = serializers.serialize('json', v)

    # server_list = models.Server.objects.values('id', 'hostname', 'create_at')
    server_list = models.Server.objects.values(*values_list)
    # 注意这里要list一下，queryset对象是不可以进行json序列化的
    # 否则会报错Object of type 'QuerySet' is not JSON serializable
    # 但是如果说取出来的v里面包含datetime对象的话也是不能序列化的，还是会报错
    # 因此需要对这个json模块进行扩展

    class JsonCustomEncoder(json.JSONEncoder):

        def default(self, value):
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, value)
    ret = {
        'server_list': list(server_list),
        'table_config': table_config,
    }
    # 这里可以加一个参数cls，这样在每一个字段序列化的时候都会调用这个类的特殊方法
    # 默认这个cls不填的话就是json.JSONEncoder
    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))
