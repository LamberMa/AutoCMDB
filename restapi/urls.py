#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 下午5:28
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, re_path
from restapi import views

urlpatterns = [
    re_path(r'^servers/$', views.ServerView.as_view()),
    re_path(r'^servers/(\d+)/$', views.ServerDetail.as_view()),
]
