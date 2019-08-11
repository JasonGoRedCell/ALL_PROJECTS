
from django.http import HttpResponse
from django.shortcuts import render
import os
from django.conf import settings

def test_cookie(request):
    resp = HttpResponse("OK")
    # ..在此处设置和修改cookie
    # 添加和修改Cookies
    # resp.set_cookie('myschool', 'abcd', max_age=7*24*60*60)
    # 删除和Cookies
    resp.delete_cookie('myschool')
    # 修改Cookies

    return resp

def show_cookie(request):
    dic = request.COOKIES
    return HttpResponse(str(dic))


def test_session(request):
    # 为session 添加mykey 对应的值
    # request.session['mykey'] = ['北京', '上海']
    # 改
    # request.session['mykey'] = "hello"
    # 删除
    del request.session['mykey']

    return HttpResponse('设置成功')


def show_session(request):
    # 取出sesssion中,mykey对应的数据
    value = request.session.get('mykey', 'mykey没有对应的值')
    s = str(value)
    return HttpResponse(s)


def show_homepage(request):
    return render(request, 'homepage.html', locals())

def on_upload(request):
    if request.method == 'GET':
        return render(request,'upload.html')
    elif request.method == 'POST':
        myfile = request.FILES['myfile']
        print("file:",myfile)
        print("您刚才上传的文件名为:",myfile.name)
        with open(os.path.join(settings.UPLOAD_DIR
                  ,myfile.name),'wb') as f:
            b = myfile.file.read()
            f.write(b)
        return HttpResponse("文件上传成功")













