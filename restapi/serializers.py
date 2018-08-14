#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 下午5:46
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers


class MySer(serializers.Serializer):
    # 相当于写了一个form组件，其实就是
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    email = serializers.CharField()