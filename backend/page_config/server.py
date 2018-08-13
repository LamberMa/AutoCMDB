#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午12:09
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : server.py
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
        },
        'attrs': {
        }
    },
    {
        'q': 'hostname',
        'title': '主机名',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {'n1': '@hostname'},
        },
        'attrs': {
            'edit-enable': 'true',
            # 添加原来的字段用于比较是否做过修改
            'origin': '@hostname',
            # 因为最后提交过来要插入到数据库，因此需要明确插入的字段。
            'name': 'hostname',
        }
    },
    {
        'q': 'create_at',
        'title': '创建时间',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {'n1': '@create_at'},
        },
        'attrs': {
            'edit-enable': 'false',
        }
    },
    {
        'q': 'asset__cabinet_num',
        'title': '机柜号',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {'n1': '@asset__cabinet_num'},
        },
        'attrs': {
            'edit-enable': 'true',
            'origin': '@asset_cabinet_num',
            'name': 'xxx',
        }
    },
    {
        'q': 'asset__business_unit__name',
        'title': '业务线名称',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {'n1': '@asset__business_unit__name'},
        },
        'attrs': {
            'edit-enable': 'true',

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
