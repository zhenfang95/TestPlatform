from django.shortcuts import render

# Create your views here.
#HttpResponse用来返回一个字符串的，HttpResponseRedirect是用来重定向到其他url上，render是用来返回html页面和页面初始数据
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

def welcome(request):
    print('进来啦……')
    return render(request,'welcome.html')