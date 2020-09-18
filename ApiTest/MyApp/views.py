# Create your views here.
#HttpResponse用来返回一个字符串的，HttpResponseRedirect是用来重定向到其他url上，render是用来返回html页面和页面初始数据
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required    #登录态检查
from MyApp.models import *

@login_required
def welcome(request):
    return render(request,'welcome.html')


def child_json(eid):
    #返回表中所有超链接
    date = DB_home_href.objects.all()
    res = {"hrefs":date} #给前端返回一个字典（前端格式要求只是是字典）
    return res

#返回子页面,控制不同的页面返回不同的数据：数据分发器
def child(request,eid,oid):      #eid是我们进入的html文件名字
    if eid == 'Home.html':
        res = child_json(eid)
        child1 = render(request,eid,res)
    else:
        child1 = render(request,eid)
    return child1

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




