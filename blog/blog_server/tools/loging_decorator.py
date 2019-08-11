
# *methods - 可接受 任意参数
# **kwargs - 可接受 多个 key=value 形式的参数
import jwt
from django.http import JsonResponse

from user.models import UserProfile

KEY = 'abcdef1234'

def loging_check(*methods):
    def _loging_check(func):
        def wrapper(request, *args, **kwargs):
            # token 放在 request header -> authorization
            # token = request.META.get('HTTP_AUTHORIZATION')
            token = request.META.get('HTTP_AUTHORIZATION')
            if not methods:
                #如果没传methods参数，则直接返回视图
                return func(request, *args, **kwargs)
            #mehtods 有值
            if not request.method in methods:
                #如果当前请求的方法不在 methods内，则直接返回视图
                return func(request, *args, **kwargs)
            #严格判断参数大小写，统一大写
            #严格检查methods里的参数是 POST,GET,PUT,DELETE

            # token校验 '
            if not token or token == 'null':
                result = {'code':107, 'error': 'Please give me token' }
                return JsonResponse(result)
            # 校验token , pyjwt 注意 异常检测
            try:
                #pyjwt deocde -> 验证token
                res = jwt.decode(token, KEY, algorithms='HS256')
            except Exception as e:
                print('---token error is %s'%(e))
                result = {'code': 108, 'error': 'Please login'}
                return JsonResponse(result)
            # token 校验成功， 根据用户名取出用户
            username = res['username']
            user = UserProfile.objects.get(username=username)
            # request.user = user
            request.user = user
            return func(request, *args, **kwargs)
        return wrapper
    return _loging_check


def get_user_by_request(request):
    '''
    通过request 获取 用户[温柔]
    :param request:
    :return: user对象 or None
    '''
    token = request.META.get('HTTP_AUTHORIZATION')
    #检查token
    if not token or token == 'null':
        return None

    try:
        res = jwt.decode(token, KEY, algorithms='HS256')
    except Exception as e:
        print('--get_user_by_request -jwt decode error is %s'%(e))
        return  None
    #获取token中的用户名
    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user







