from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.users, name='users'),
    #/v1/users/guoxiaonao
    url(r'^/(?P<username>[\w]{1,11})$', views.users, name='user'),
    #/v1/users/guoxiaonao/avatar
    url(r'^/(?P<username>[\w]{1,11})/avatar$', views.user_avatar, name='user_avatar')
]