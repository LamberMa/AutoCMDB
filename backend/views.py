import json
from datetime import datetime, date

from django.shortcuts import render, HttpResponse
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

        values_list = [row['q'] for row in server_table_config if row['q']]
        server_list = models.Server.objects.values(*values_list)
        search_config = [
            {'name': 'cabinet_num', 'text': '机柜号', 'search_type': 'input'},
            {'name': 'device_type_id', 'text': '资产类型', 'search_type': 'select', 'global_name': 'device_type_choices'},
            {'name': 'device_status_id', 'text': '资产状态', 'search_type': 'select', 'global_name': 'device_status_choices'},
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

    values_list = [row['q'] for row in asset_table_config if row['q']]
    asset_list = models.Asset.objects.values(*values_list)

    ret = {
        'server_list': list(asset_list),
        'table_config': asset_table_config,
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
