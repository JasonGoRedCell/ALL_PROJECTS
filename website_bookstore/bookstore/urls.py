# 创建文件: bookstore/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^add$', views.new_book),
    url(r'^list_all$', views.list_books),
    url(r'^mod/(\d+)$', views.mod_book_info),
    url(r'^del/(\d+)$', views.del_book),
    url(r'^book', views.books_page, name='book'),
]










