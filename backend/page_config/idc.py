#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午12:11
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : idc.py
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
        'q': 'name',
        'title': '机房名称',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {'n1': '@name'},
        },
        'attrs': {
            'edit-enable': 'true',
            'origin': '@name',
            'name': 'name',
        }
    },
    {
        'q': 'floor',
        'title': '机房楼层',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {'n1': '@floor'},
        },
        'attrs': {
            'edit-enable': 'true',
            'origin': '@floor',
            'name': 'floor',
        }
    },
]
