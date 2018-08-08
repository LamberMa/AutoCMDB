import json
import hashlib
import time
from django.shortcuts import render, HttpResponse
from repository import models
from django.conf import settings

api_key_record = {
    # "1b96b89695f52ec9de8292a5a7945e38|1501472467.4977243":1501472477.4977243
}


def asset(request):
    """
    server_info: 拿到的新资产信息
    server_obj: 旧的资产信息
    作业：通过反射实现插件入库
    验证规则改为装饰器。
    设计灵感参考tornado中加密cookie类似灵感。
    :param request:
    :return:
    """
    if request.method == "GET":
        client_md5_key, client_ctime = request.META.get('HTTP_OPENKEY').split('|')
        server_time = time.time()
        # 第一关
        # 干掉10s以外的所有过期请求，但是黑客可以改时间，但是时间改了md5值就变了，所以仍然过不去
        if server_time - float(client_ctime) > 10:
            return HttpResponse('【第一关】小伙子，别唬我，太长了')

        # 第二关
        auth_str = "%s|%s" % (settings.AUTH_KEY, client_ctime)
        m = hashlib.md5()
        m.update(bytes(auth_str, encoding='utf-8'))
        auth_code = m.hexdigest()
        if auth_code != client_md5_key:
            # 因为第一关黑客可能通过修改时间蒙混过关，但是时间一改，md5就变了，所以这一关避不了
            return HttpResponse('【第二关】小子，你是不是修改时间了')

        for k in list(api_key_record.keys()):
            v = api_key_record[k]
            if server_time > v:
                del api_key_record[k]
    elif request.method == 'POST':
        # 新资产信息，这个资产是从request.body拿过来的。
        server_info = json.loads(request.body.decode('utf-8'))
        hostname = server_info['basic']['data']['hostname']
        # 老资产信息，旧的Server对象
        server_obj = models.Server.objects.filter(hostname=hostname).first()

        if not server_obj:
            return HttpResponse('当前主机名在资产中未录入')
        asset_obj = server_obj.asset

        # 首先处理硬盘的更新信息
        if server_info['disk']['status']:
            # 我们抓取过来的新信息是字典个事的
            new_disk_data = server_info['disk']['data']
            # 旧的硬盘信息其实是从数据库取出来的一个个Disk模型类的对象
            old_disk_data = models.Disk.objects.filter(server_obj=server_obj)

            # 交集：5, 创建：3,删除4;
            # 新发过来的新采集的数据有多少个硬盘的槽位，比如：['0', '1', '2', '3', '4', '5']
            new_slot_list = list(new_disk_data.keys())
            # 新建一个旧的disk槽位列表，循环取到的旧信息把所有的slot拿出来放到列表。
            old_slot_list = []
            for item in old_disk_data:
                # 循环每一个旧的disk对象
                old_slot_list.append(item.slot)

            """
            比如新获取的槽位，我们放到列表以后有0，1，2，3，4，5六个槽位。旧的槽位只有0，1，2，6
            - 新增的数据：3，4，5
            - 可能需要更新的数据：0，1，2
            旧的需要删除的就是6.针对这几个数据，我们可以使用集合的交集，差集。
            """
            # 更新列表，取二者都有的，进行更新
            update_list = set(new_slot_list).intersection(old_slot_list)
            # 新增列表，取新的有的，旧的没有的，差集。
            create_list = set(new_slot_list).difference(old_slot_list)
            # 删除列表，取旧的有的，新的没有的，差集。
            del_list = set(old_slot_list).difference(new_slot_list)

            # 如果删除列表存在的话
            if del_list:
                models.Disk.objects.filter(server_obj=server_obj, slot__in=del_list).delete()
                # 记录日志
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除硬盘：%s" % ("、".join(del_list),))
            # 增加、
            record_list = []
            for slot in create_list:
                """
                每一个slot信息是一个小字典
                {
                    'slot': '5', 
                    'pd_type': 'SATA', 
                    'capacity': '476.939', 
                    'model': 'S1AXNSAFB00549A  Samsung SSD 840 PRO Series DXM06B0Q'
                }
                """
                disk_dict = new_disk_data[slot]
                disk_dict['server_obj'] = server_obj
                # 这里为了方便创建，因此在设计上，模型类和抓取到的key字段是一致的。
                models.Disk.objects.create(**disk_dict)
                temp = "新增硬盘:位置{slot},容量{capacity},型号:{model},类型:{pd_type}".format(**disk_dict)
                record_list.append(temp)
            if record_list:
                content = ";".join(record_list)
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

            # ############ 更新 ############
            record_list = []
            row_map = {'capacity': '容量', 'pd_type': '类型', 'model': '型号'}
            for slot in update_list:
                new_dist_row = new_disk_data[slot]
                old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=server_obj).first()
                for k, v in new_dist_row.items():
                    # k: capacity;slot;pd_type;model
                    # v: '476.939''xxies              DXM05B0Q''SATA'
                    # 通过反射拿到对象里的值，然后和新的值做比对，比对的目的是将资产变更记录入库
                    value = getattr(old_disk_row, k)
                    # 值不相等把不相等的部分记录下来
                    if v != value:
                        record_list.append("槽位%s,%s由%s变更为%s" % (slot, row_map[k], value, v,))
                        setattr(old_disk_row, k, v)
                    # 然后把重新设置的数据行直接保存就可以了。
                    old_disk_row.save()
                if record_list:
                    content = ";".join(record_list)
                    models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        else:
            models.ErrorLog.objects.create(content=server_info['disk']['data'],
                                           asset_obj=server_obj.asset,
                                           title='【%s】硬盘采集错误信息' % hostname)

        # 资产表中以前资产信息
        # server_obj可以找到服务基本信息（单条）
        # disk_list = server_obj.disk.all()



        # 处理：
        """
        1. 根据新资产和原资产进行比较：新["5","1"]      老["4","5","6"]
        构造集合，交集有的更新，新的有的，旧的没有的j增加，旧的有的，新的没有的就删除。
        2. 增加: [1,]   更新：[5,]    删除：[4,6]
        3. 增加：
                server_info中根据[1,],找到资产详细：入库
           删除：
                数据库中找当前服务器的硬盘：[4,6]

           更新：[5,]
                disk_list = [obj,obj,obj]

                {
                    'data': {
                        '5': {'slot': '5', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'},
                        '3': {'slot': '3', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'},
                        '4': {'slot': '4', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'},
                        '0': {'slot': '0', 'capacity': '279.396', 'pd_type': 'SAS', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'},
                        '2': {'slot': '2', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'},
                        '1': {'slot': '1', 'capacity': '279.396', 'pd_type': 'SAS', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}
                    },

                    'status': True
                }

                log_list = []

                dict_info = {'slot': '5', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'},
                obj
                    if obj.capacity != dict_info['capacity']:
                        log_list.append('硬盘容量由%s变更为%s' %s(obj.capacity,dict_info['capacity'])
                        obj.capacity = dict_info['capacity']
                    ...
                obj.save()

                models.xxx.object.create(detail=''.join(log_list))

        """


            # 今天作业：(基本信息，硬盘，内存)

    return HttpResponse('...')
