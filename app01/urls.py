# /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/30 14:54 
# @Author : TrueNewBee
from django.conf.urls import url
from app01 import views


urlpatterns = [
    url(r"manage_article/$", views.manage_article),            # 编辑文章的url
    url(r"add_article/", views.add_article),            # 添加文章的url
    url(r"up_down/", views.up_down),                    # 点赞的url
    url(r"comment/", views.comment),                    # 评论的url
    url(r"comment_tree/(\d+)/", views.comment_tree),    # 评论树的url
    # /blog/xiaohei/tag/python
    # /blog/xiaohei/category/技术
    # /blog/xiaohei/archive/2018-05
    # url(r'(\w+)/tag/(\w+)', views.tag),
    # url(r'(\w+)/category/(\w+)', views.category),
    # url(r'(\w+)/archive/(.+)', views.archive),
    # 三和一 URL

    url(r'(\w+)/(tag|category|archive)/(.+)/', views.home),  # 个人详情页面 home(request, username, tag, 'python')

    url(r'(\w+)/article/(\d+)/$', views.article_detail),  # 文章详情  article_detail(request, xiaohei, 1)

    url(r'(\w+)', views.home),  # home(request, username)
]
