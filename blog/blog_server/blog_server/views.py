from django.http import JsonResponse

from user.models import UserProfile
import redis


def test_api(request):
    #JsonResponse 1,将返回内容序列化成json
    #2,response中添加 content-type: application/json
    # return JsonResponse({'code':200})

    import redis
    pool = redis.ConnectionPool(
        host = 'localhost',
        port = 6379,
        db = 0
    )
    r = redis.Redis(connection_pool=pool)
    # 加入redis分布式锁
    # set key value nx
    # del key
    try:
        with r.lock('jasongo',blocking_timeout=3) as lock:
            u = UserProfile.objects.get(username='jasongo')
            u.score += 1
            u.save()
    except Exception as e:
        print(e,'lock is failed')
    return JsonResponse({'msg':'test is ok'})
