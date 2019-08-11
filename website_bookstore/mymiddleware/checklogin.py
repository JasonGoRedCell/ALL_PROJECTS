
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.utils.deprecation import MiddlewareMixin

import re

class MyMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        print("中间件MyMiddleWare.process_request方法被调用")
        if re.match(r'^/bookstore', request.path_info) \
                and ('userinfo' not in request.session):
            return HttpResponseRedirect('/userinfo/login')
        return None

