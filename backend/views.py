import json
from datetime import datetime, date

from django.shortcuts import render, HttpResponse
from django.db.models import Q

from repository import models
from backend.page_config.server import table_config as server_table_config
from backend.page_config.idc import table_config as idc_table_config
from backend.page_config.asset import table_config as asset_table_config


class JsonCustomEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)


def get_data_list(request, table_config, model_cls):
    con = Q()
    condition = request.GET.get('condition')
    condition_dict = json.loads(condition)
    print(condition_dict)
    for name, values in condition_dict.items():
        ele = Q()
        ele.connector = 'OR'
        for item in values:
            ele.children.append((name, item))
        con.add(ele, 'AND')
    values_list = [row['q'] for row in table_config if row['q']]
    server_list = model_cls.objects.filter(con).values(*values_list)
    return server_list


def curd(request):
    return render(request, 'backend/curd.html')


def curd_json(request):
    if request.method == "DELETE":
        # 为什么用request.body，因为只有request.get和request.post，其他的一律在body中自己处理
        # request.body.decode('utf-8')，或者用下面的方法
        # 删除的时候直接删除id_list就行了。有了批量删除以后，后面的操作就啥用了，也可以留着
        id_list = json.loads(str(request.body, encoding='utf-8'))
        return HttpResponse('...')
    elif request.method == "POST":
        return HttpResponse('...')
    elif request.method == 'PUT':
        # print(request.body)
        all_list = json.loads(request.body.decode('utf-8'))
        for row in all_list:
            nid = row.pop('id')
            models.Server.objects.filter(id=nid).update(**row)
        return HttpResponse('...')
    else:
        # 注意这里还是可以跨表的，可以动态的放在用户的cookie里。

        server_list = get_data_list(request, server_table_config, models.Server)

        search_config = [
            # 使用xxx__contains做模糊匹配，orm的用法再回顾一下。
            {'name': 'hostname__contanins', 'text': '主机名', 'search_type': 'input'},
            {'name': 'sn__contains', 'text': 'SN号', 'search_type': 'input'},
            # {'name': 'cabinet_num', 'text': '机柜号', 'search_type': 'input'},
            # {'name': 'device_type_id', 'text': '资产类型', 'search_type': 'select', 'global_name': 'device_type_choices'},
            # {'name': 'device_status_id', 'text': '资产状态', 'search_type': 'select', 'global_name': 'device_status_choices'},
        ]

        ret = {
            'server_list': list(server_list),
            'table_config': server_table_config,
            'search_config': search_config,
            # 注意这里是不应该有这个global信息的，只是目前保证数据的显示而已。因为server表中名没有什么choices
            'global_dict': {
                'device_type_choices': models.Asset.device_type_choices,
                'device_status_choices': models.Asset.device_status_choices,
            },
        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def asset(request):
    return render(request, 'backend/asset.html')


def asset_json(request):
    if request.method == "DELETE":
        pass
    elif request.method == "GET":
        pass
    elif request.method == 'PUT':
        # print(request.body)
        all_list = json.loads(request.body.decode('utf-8'))
        print(all_list)
        # for row in all_list:
        #     nid = row.pop('id')
        #     models.Asset.objects.filter(id=nid).update(**row)
        return HttpResponse('...')
    asset_list = get_data_list(request, asset_table_config, models.Asset)

    search_config = [
        # 使用xxx__contains做模糊匹配，orm的用法再回顾一下。
        {'name': 'cabinet_num', 'text': '机柜号', 'search_type': 'input'},
        {'name': 'device_type_id', 'text': '资产类型', 'search_type': 'select', 'global_name': 'device_type_choices'},
        {'name': 'device_status_id', 'text': '资产状态', 'search_type': 'select', 'global_name': 'device_status_choices'},
    ]

    ret = {
        'server_list': list(asset_list),
        'table_config': asset_table_config,
        'search_config': search_config,
        # 如果让前端拿到id对应的状态（类型）值呢，其实就是把所有的值把过去让前端去遍历
        # 然后匹配的填上值就行了，因为这些操作的处理逻辑都是一致的，因此统一扔到一个global_dict中
        # 拿过来的这些都是元组，元组经过json序列化以后都是列表了。
        'global_dict': {
            'device_type_choices': models.Asset.device_type_choices,
            'device_status_choices': models.Asset.device_status_choices,
            'idc_choices': list(models.IDC.objects.values_list('id', 'name')),
        },
    }

    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def idc(request):
    return render(request, 'backend/idc.html')


def idc_json(request):
    if request.method == "DELETE":
        id_list = json.loads(request.body.decode('utf-8'))
        print(id_list)
        return HttpResponse('...')
    elif request.method == "PUT":
        all_list = json.loads(request.body.decode('utf-8'))
        print(all_list)
        return HttpResponse('...')
    elif request.method == 'GET':
        values_list = [row['q'] for row in idc_table_config if row['q']]
        idc_list = models.IDC.objects.values(*values_list)

        ret = {
            'server_list': list(idc_list),
            'table_config': idc_table_config,
            'global_dict': {
            },
        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def chart(request):
    return render(request, 'backend/chart.html')
