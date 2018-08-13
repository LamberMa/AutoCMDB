#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午12:11
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : asset.py
# @Software: PyCharm


table_config = [
        {
            'q': None,
            'title': '选择',
            'display': True,
            'text': {
                'tpl': '<input type="checkbox" value="{n1}">',
                'kwargs': {'n1': '@id'}
            },
            'attrs': {
                'edit-enable': 'false',
            }
        },
        {
            'q': 'id',
            'title': 'ID',
            'display': False,
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@id'},
            }
        },
        {
            'q': 'device_type_id',
            'title': '资产类型',
            'display': True,
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@@device_type_choices'},
            },
            'attrs': {
                'edit-enable': 'true',
                'edit-type': 'select',
                'global-key': 'device_type_choices',
                'origin': '@device_type_id'
            }
        },
        {
            'q': 'device_status_id',
            'title': '状态',
            'display': True,
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@@device_status_choices'},
            },
            'attrs': {
                'edit-enable': 'true',
                'edit-type': 'select',
                'global-key': 'device_status_choices',
                'origin': '@device_status_id',
            }
        },
        {
            'q': 'cabinet_num',
            'title': '机柜号',
            'display': True,
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@cabinet_num'},
            },
            'attrs': {
                'edit-enable': 'true',
            }
        },
        {
            'q': 'idc__id',
            'title': '机房',
            'display': None,
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@idc__id'},
            },
        },
        {
            'q': 'idc__name',
            'title': '机房',
            'display': True,
            'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@idc__name'},
            },
            'attrs': {
                'edit-enable': 'true',
                'origin': '@idc__id',
                'edit-type': 'select',
                'global-key': 'idc_choices'
            }
        },
        {
            'q': None,
            'title': '操作',
            'display': True,
            'text': {
                'tpl': '<a href="/backend/del?nid={nid}">删除</a>',
                'kwargs': {'nid': '@id'},
            },
            'attrs': {
                'edit-enable': 'false',
            }
        },
    ]