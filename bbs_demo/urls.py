"""bbs_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from app01 import views
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from app01 import urls as blog_urls
"""
super_user :  root    zhen1996.....
"""
urlpatterns = [
    url(r'^$', views.music),
    url(r'^admin/', admin.site.urls),
    url(r'^up/$', views.up),            # 这是一个上传的demo
    # 专门用来校验用户名是否已被注册的接口
    url(r'^check_username_exist/$', views.check_username_exist),
    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register', views.get_geetest),

    url(r'^login/$', views.login),      # 用户登入页面    星期天用我自己的用户登入
    url(r'^reg/$', views.register),     # 这是用户注册的页面
    url(r'^index/$', views.index),      # 这是一个index 页面
    url(r'^logout/$', views.logout),    # 这是一个注销页面

    # media相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    # 将所有以blog开头的url都交给app1 下面的urls.py 处理
    url(r'^blog/', include(blog_urls)),
    # 在添加文章时候上传文件url
    url(r'^upload/', views.upload),

]
