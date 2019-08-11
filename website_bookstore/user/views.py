from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def mylogin2(request):
    if request.method == 'GET':
        return render(request,'user/login.html',locals())
    elif request.method == 'POST':
        return HttpResponse("登录失败")