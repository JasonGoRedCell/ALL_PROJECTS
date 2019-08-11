"""blog_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test_api', views.test_api),
    #添加user模块 url映射
    url(r'v1/users', include('user.urls')),
    #添加btoken模块 url映射, 该模块用登录操作
    url(r'v1/token', include('btoken.urls')),
    #添加topic模块 url映射
    url(r'v1/topics', include('topic.urls')),
    #添加message模块 url映射
    url(r'v1/messages', include('message.urls'))
]

#from django.conf import settings
#from django.conf.urls.static import static
#添加图片路由映射 http://127.0.0.1:8000/media/aaa.jpg
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






