# Create your views here.
#HttpResponse用来返回一个字符串的，HttpResponseRedirect是用来重定向到其他url上，render是用来返回html页面和页面初始数据
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required    #登录态检查
from MyApp.models import *

@login_required
def welcome(request):
    return render(request,'welcome.html')

#控制不同的页面返回不同的数据：数据分发器
def child_json(eid,oid=''):
    res={}
    if eid == 'Home.html':
        #返回表中所有数据
        date = DB_home_href.objects.all()
        res = {"hrefs":date}    #给前端返回一个字典格式
    if eid == 'project_list.html':
        date = DB_project.objects.all()
        res = {'projects':date}
    if eid == 'P_apis.html':
        project_name = DB_project.objects.filter(id=oid)[0].name
        res = {'project_name':project_name}
    return res

#返回子页面
def child(request,eid,oid):      #eid是我们进入的html文件名字,oid是用来区分数据的参数
    res = child_json(eid,oid)
    return render(request,eid,res)

#进入主页
@login_required
def home(request):
    return render(request,'welcome.html',{"whichHTML": "Home.html","oid": ""})   #返回主页Home.html给前端

#进入登录页面
def login(request):
    return render(request,'login.html')

#登陆
def login_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    #连Django用户库，查看用户名/密码是否正确
    from django.contrib import auth
    user = auth.authenticate(username=u_name,password=p_word)
    if user is not None:
        auth.login(request,user)   #检查用户是否已登录
        request.session['user'] = u_name  #记录用户登录态
        return HttpResponse('成功')
    else:
        #返回前端告诉前端用户名/密码不对
        return HttpResponse('失败')
#注册
def register_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    #连通Django用户表
    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username=u_name,password=p_word)
        user.save()
        return HttpResponse('注册成功')
    except:
        return HttpResponse('注册失败,用户已存在……')

#退出登录
def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return HttpResponseRedirect('/login/')

#所用请求信息包括请求者的登陆用户名都存放在request参数中，如：user.username就是请求的用户名
#吐槽框
def submit(request):
    tucao_text = request.GET['tucao_text'] #获取吐槽内容
    #利用create方法创建数据库记录
    DB_tucao.objects.create(user=request.user.username,text=tucao_text) #吐槽内容写入表中
    return HttpResponse('提交成功！')

#帮助文档
def api_help(request):
    return render(request,'welcome.html',{"whichHTML": "Help.html","oid": ""})

#项目列表
def project_list(request):
    return render(request,'welcome.html',{"whichHTML":"project_list.html","oid":""})

#删除项目
def delete_project(request):
    id = request.GET['id']
    #根据id删除表中数据
    DB_project.objects.filter(id=id).delete()   #filter()是找出所有符合的数据
    return HttpResponse('项目已删除!')

#新增项目
def add_project(request):
    project_name = request.GET['project_name']
    project_remark = request.GET['project_remark']
    #新增一条项目数据
    DB_project.objects.create(name=project_name,remark=project_remark,user=request.user.username,other_user='')
    return HttpResponse('项目已添加')

#进入接口库
def open_apis(request,id):
    project_id = id
    return render(request,'welcome.html',{"whichHTML":"P_apis.html","oid":project_id})

#进入用例设置
def open_cases(request,id):
    project_id = id
    return render(request,'welcome.html',{"whichHTML":"P_cases.html","oid":""})

#进入项目设置
def open_project_set(request,id):
    project_id = id
    return render(request,'welcome.html',{"whichHTML":"P_project_set.html","oid":""})