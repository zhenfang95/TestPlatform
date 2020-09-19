"""ApiTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from MyApp.views import *

#路由控制器，逻辑：库函数('你的url 1'，‘你的后台函数名1 ’)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^welcome/$',welcome),  #进入主页,^是正则匹配写法
    url(r'^home/$',home),
    url(r'^child/(?P<eid>.+)/(?P<oid>.*)/$',child),  #返回子页面（正则表达式写法）
    url(r'^login/$',login),
    url(r'^login_action/$',login_action),
    url(r'^register_action/$',register_action),
    url(r'^accounts/login/$',login),
    url(r'^logout/$',logout),
    url(r'^submit/$',submit),
    url(r'^help/$',api_help),
    url(r'^project_list/$',project_list),
]
