# Create your views here.
from django.shortcuts import render

# Create your views here.

# userinfo/views.py
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import models

def mylogin(request):
    if request.method == 'GET':
        username = request.COOKIES.get('username', '')
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        # 获取表单的数据
        remember = request.POST.get('remember', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 验证用户名，密码是否正确
        try:
            user = models.User.objects.get(name=username,
                                           password=password)
            # 在当前连接的Session中记录当前用户的信息
            request.session['userinfo'] = {
                "username": user.name,
                'id': user.id
            }
        except:
            return HttpResponse("登陆失败")

        # 处理COOKIES
        resp = HttpResponseRedirect('/note/home')
        if remember:
            resp.set_cookie('username', username, 7*24*60*60)
        else:
            resp.delete_cookie('username')
        return resp


def myregister(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if username == '':
            username_error = "用户名不能为空"
            return render(request, 'register.html', locals())
        if password == '':
            return HttpResponse("密码不能为空")
        if password != password2:
            return HttpResponse('两次密码不一致!')
        # 开始注册功能
        try:
            from . import models
            user = models.User.objects.create(
                name=username,
                password=password
            )
            return HttpResponse("注册成功")
        except:
            return HttpResponse("注册失败")


def mylogout(request):
    '退出登陆'
    if 'userinfo' in request.session:
        del request.session['userinfo']
    return HttpResponseRedirect('/')  # 注销后跳转到主页
