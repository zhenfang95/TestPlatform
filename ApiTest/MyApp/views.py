# Create your views here.
#HttpResponse用来返回一个字符串的，HttpResponseRedirect是用来重定向到其他url上，render是用来返回html页面和页面初始数据
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required    #登录态检查

@login_required
def welcome(request):
    return render(request,'welcome.html')

#返回子页面
def child(request,eid,oid):
    return render(request,eid)

#进入主页
@login_required
def home(request):
    return render(request,'welcome.html',{"whichHTML": "Home.html","oid": ""})

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

def case_list(request):
    return HttpResponse('测试用例列表……')

def item_list(request):
    return HttpResponse('项目列表……')

def portlib(request):
    return HttpResponse('接口库……')