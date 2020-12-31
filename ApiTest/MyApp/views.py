# Create your views here.
#HttpResponse用来返回一个字符串的，HttpResponseRedirect是用来重定向到其他url上，render是用来返回html页面和页面初始数据
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required    #登录态检查
from MyApp.models import *
import json
import requests

@login_required
def welcome(request):
    return render(request,'welcome.html')

#控制不同的页面返回不同的数据：数据分发器
def child_json(eid,oid='',ooid=''):
    res={}
    if eid == 'Home.html':
        #返回表中所有数据
        date = DB_home_href.objects.all()
        home_log = DB_apis_log.objects.filter(user_id=oid)[::-1]
        # 给前端返回一个字典格式
        if ooid == '':
            res = {"hrefs":date,"home_log":home_log}
        else:
            log = DB_apis_log.objects.filter(id=ooid)[0]
            res = {"hrefs":date,"home_log":home_log,"log":log}

    if eid == 'project_list.html':
        date = DB_project.objects.all()
        res = {'projects':date}
    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}
    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}
    if eid == 'P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}
    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)
        res = {'project':project,'apis':apis}
    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        Cases = DB_cases.objects.filter(project_id=oid)
        res = {"project":project,"Cases":Cases}

    return res

#返回子页面
def child(request,eid,oid,ooid):      #eid是我们进入的html文件名字,oid是用来区分数据的参数
    res = child_json(eid,oid,ooid)
    return render(request,eid,res)

#进入主页
@login_required
def home(request,log_id=''):
    return render(request,'welcome.html',{"whichHTML": "Home.html","oid": request.user.id,"ooid":log_id})   #返回主页Home.html给前端

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
    DB_apis.objects.filter(project_id=id).delete()
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
    return render(request,'welcome.html',{"whichHTML":"P_cases.html","oid":project_id})

#进入项目设置
def open_project_set(request,id):
    project_id = id
    return render(request,'welcome.html',{"whichHTML":"P_project_set.html","oid":project_id})

#保存项目设置
def save_project_set(request,id):
    project_id = id
    name = request.GET['name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']
    DB_project.objects.filter(id=project_id).update(name=name,remark=remark,other_user=other_user)
    return HttpResponse('保存成功')

#新增接口
def project_api_add(request,Pid):
    project_id = Pid
    DB_apis.objects.create(project_id=project_id,api_method='none')
    return HttpResponseRedirect('/apis/%s'%project_id)

#删除接口
def project_api_del(request,id):
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    DB_apis.objects.filter(id=id).delete()
    return HttpResponseRedirect('/apis/%s'%project_id)


#保存备注
def save_bz(request):
    api_id = request.GET['api_id']
    bz_value = request.GET['bz_value']
    DB_apis.objects.filter(id=api_id).update(des=bz_value)
    return HttpResponse('')

#获取备注
def get_bz(request):
    api_id = request.GET['api_id']
    bz_value = DB_apis.objects.filter(id=api_id)[0].des
    return HttpResponse(bz_value)

#保存接口
def Api_save(request):
    #提取所有数据
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    api_name = request.GET['api_name']
    ts_body_method = request.GET['ts_body_method']

    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
    else:
        ts_api_body = request.GET['ts_api_body']

    #保存数据
    DB_apis.objects.filter(id=api_id).update(
        api_method = ts_method,
        api_url = ts_url,
        api_header = ts_header,
        api_host = ts_host,
        body_method = ts_body_method,
        api_body = ts_api_body,
        name = api_name
    )
    return  HttpResponse('success')

#获取接口数据
def get_api_data(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api),content_type='application/json')  #返回json格式数据给前端

#调式层发送请求
def Api_send(request):
    #提取所有数据
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    api_name = request.GET['api_name']
    ts_body_method = request.GET['ts_body_method']

    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
        if ts_body_method in ['',None]:
            return HttpResponse('请先选择好请求方式和请求体，再点击Send按钮发送请求')
    else:
        ts_api_body = request.GET['ts_api_body']
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method,last_api_body=ts_api_body)

    #发送请求获取返回值
    try:
        header = json.loads(ts_header) #请求头
    except:
        return HttpResponse('请求头不符合json格式')
    #拼接完整的url
    if ts_host[-1] == '/' and ts_url[0] == '/':   #都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  #都没有/
        url = ts_host + '/' + ts_url
    else:
        url = ts_host + ts_url
    try:
        if ts_body_method == 'none':
            response = requests.request(ts_method.upper(), url, headers=header, data={})

        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(),url,headers=header,data=payload,files=files)

        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(),url,headers=header,data=payload)
        else:
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'
            elif ts_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'
            elif ts_body_method == 'Json':
                header['Content-Type'] = 'application/json'
            elif ts_body_method == 'Html':
                header['Content-Type'] = 'text/plain'
            elif ts_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))

        #把返回值传递给前端页面
        response.encoding = "utf-8"
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))

#复制接口
def copy_api(request):
    api_id = request.GET['api_id']
    #开始复制接口
    old_api = DB_apis.objects.filter(id=api_id)[0]
    DB_apis.objects.create(project_id=old_api.project_id,
                           name=old_api.name+ '_copy',
                           api_method=old_api.api_method,
                           api_url = old_api.api_url,
                           api_header=old_api.api_header,
                           api_login=old_api.api_login,
                           api_host=old_api.api_host,
                           des=old_api.des,
                           body_method=old_api.body_method,
                           api_body=old_api.api_body,
                           result=old_api.result,
                           sign=old_api.sign,
                           file_key=old_api.file_key,
                           file_name=old_api.file_name,
                           public_header=old_api.public_header,
                           last_body_method=old_api.last_body_method,
                           last_api_body=old_api.last_api_body
                           )
    return HttpResponse('')

#异常值发送请求
def error_request(request):
    api_id = request.GET['api_id']
    new_body = request.GET['new_body']
    span_text = request.GET['span_text']
    api = DB_apis.objects.filter(id=api_id)[0]
    method = api.api_method
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method
    try:
        header = json.loads(header) #请求头
    except:
        return HttpResponse('请求头不符合json格式')

    if host[-1] == '/' and url[0] == '/':  # 都有/
        url = host[:-1] + url
    elif host[-1] != '/' and url[0] !='/': #都没有/
        url = host+ '/' + url
    else: #肯定有一个有/
        url = host + url
    try:
        if body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
                response = requests.request(method.upper(), url, headers=header, data=payload, files=files)
        elif body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
                response = requests.request(method.upper(), url, headers=header, data=payload)
        elif body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            response = requests.request(method.upper(), url, headers=header, data=new_body.encode('utf-8'))
        else:
            return HttpResponse('非法的请求体类型')

        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        res_json = {"response":response.text,"span_text":span_text}
        return HttpResponse(json.dumps(res_json),content_type='application/json')
    except:
        res_json = {"response":'接口未通，请重新请求', "span_text":span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')

#首页发送请求
def Api_send_home(request):
    #提取所有数据
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    ts_api_body = request.GET['ts_api_body']
    # 发送请求获取返回值
    try:
        header = json.loads(ts_header)  # 处理header
    except:
        return HttpResponse('请求头不符合json格式！')

    # 写入到数据库请求记录表中
    DB_apis_log.objects.create(user_id=request.user.id,
                               api_method=ts_method,
                               api_url=ts_url,
                               api_header=ts_header,
                               api_host=ts_host,
                               body_method=ts_body_method,
                               api_body=ts_api_body,
                               )

    # 拼接完整url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:  # 肯定有一个有/
        url = ts_host + ts_url
    try:
        if ts_body_method == 'none':
            response = requests.request(ts_method.upper(), url, headers=header, data={})

        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)

        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)

        elif ts_body_method == 'GraphQL':
            header['Content-Type'] = 'application/json'
            query = ts_api_body.split('*WQRF*')[0]
            graphql = ts_api_body.split('*WQRF*')[1]
            try:
                int(graphql)
            except:
                graphql = '{}'
            payload = '{"query":"%s","variables":%s}' % (query, graphql)
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)


        else:  # 这时肯定是raw的五个子选项：
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Json':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Html':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))

        # 把返回值传递给前端页面
        response.encoding = "utf-8"

        #DB_host.objects.update_or_create(host=ts_host)

        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))

#首页获取请求记录
def get_home_log(request):
    user_id = request.user.id
    all_logs = DB_apis_log.objects.filter(user_id=user_id)
    ret = {"all_logs":list(all_logs.values("id","api_method","api_host","api_url"))[::-1] }
    return HttpResponse(json.dumps(ret),content_type='application/json')

#获取完整单一的请求记录数据
def get_api_log_home(request):
    log_id = request.GET['log_id']
    log = DB_apis_log.objects.filter(id=log_id)
    ret = {"log":list(log.values())[0]}
    print(ret)
    return HttpResponse(json.dumps(ret),content_type='application/json')

#增加用例
def add_case(request,eid):
    DB_cases.objects.create(project_id=eid,name='')
    return HttpResponseRedirect('/cases/%s/'%eid)