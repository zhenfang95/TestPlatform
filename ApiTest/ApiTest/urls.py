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
    url(r'^child/(?P<eid>.+)/(?P<oid>.*)/(?P<ooid>.*)/$',child),  #返回子页面（正则表达式写法）
    url(r'^login/$',login),
    url(r'^login_action/$',login_action),
    url(r'^register_action/$',register_action),
    url(r'^accounts/login/$',login),
    url(r'^logout/$',logout),
    url(r'^submit/$',submit),
    url(r'^help/$',api_help),
    url(r'^project_list/$',project_list),
    url(r'^delete_project/$',delete_project),
    url(r'^add_project/$',add_project),
    url(r'^apis/(?P<id>.*)/$',open_apis),
    url(r'^cases/(?P<id>.*)/$',open_cases),
    url(r'^project_set/(?P<id>.*)/$',open_project_set),
    url(r'^save_project_set/(?P<id>.*)/$',save_project_set),
    url(r'^project_api_add/(?P<Pid>.*)/$',project_api_add),
    url(r'^project_api_del/(?P<id>.*)/$',project_api_del),
    url(r'^save_bz/$',save_bz),
    url(r'^get_bz/$',get_bz),
    url(r'^Api_save/$',Api_save),
    url(r'^get_api_data/$',get_api_data),
    url(r'^Api_send/$',Api_send),
    url(r'^copy_api/$',copy_api),
    url(r'^error_request/$',error_request), #调用异常测试接口
    url(r'^Api_send_home/$',Api_send_home),
    url(r'^get_home_log/$',get_home_log),
    url(r'^get_api_log_home/$',get_api_log_home),
    url(r'^home_log/(?P<log_id>.*)/$',home),  #再次进入首页，这次需带着请求数据
    url(r'^add_case/(?P<eid>.*)/$',add_case),
    url(r'^del_case/(?P<eid>.*)/(?P<oid>.*)/$',del_case),
    url(r'^copy_case/(?P<eid>.*)/(?P<oid>.*)/$',copy_case),
    url(r'^get_small/$',get_small),
    url(r'^user_upload/$',user_upload),
    url(r'^add_new_step/$',add_new_step),
    url(r'^delete_step/(?P<eid>.*)/$',delete_step),
    url(r'^get_step/$',get_step),
    url(r'^save_step/$',save_step),
    url(r'^step_get_api/$',step_get_api),
    url(r'^Run_Case/$',Run_Case),
    url(r'^look_report/(?P<eid>.*)/$',look_report),
    url(r'^save_project_header/$',save_project_header),
    url(r'^save_case_name/$',save_case_name),
]
