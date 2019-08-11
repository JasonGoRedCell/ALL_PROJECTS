from django.db import models

# Create your models here.
# 判断前后端分离的金标准， 后台只返数据，数据-json
# 所有关于用户显示层面上的设计与开发 -  前端/客户端
# 前端 与 后端 之间 HTTP 协议通信， API，- RESTful
# RESTful - 1, 避免动词，尽量使用名词  2，配合HTTP method 语义
# CORS - 解决跨域的一种规范 - django-cors-headers
from user.models import UserProfile

# 迁移指定模块  - topic
# python3 manage.py makemigrations topic
# python3 manage.py migrate topic

#mysql  查询指定表的创建语句 show create table topic\G


class Topic(models.Model):
    #主键为id, django默认添加

    title = models.CharField(max_length=50, verbose_name="文章标题")
    #tec 技术类的 & no-tec 非技术类
    category = models.CharField(max_length=20,verbose_name="文章分类")
    #limit -  public 公开的 [所有人都能看] &  private 私有的 [只有文章作者本人能看]
    limit = models.CharField(max_length=10, verbose_name="文章权限")
    introduce = models.CharField(max_length=90, verbose_name="文章简介")
    content = models.TextField(verbose_name="文章内容")
    #文章创建时间
    created_time = models.DateTimeField()
    #文章修改时间
    modified_time = models.DateTimeField()
    #作者
    author = models.ForeignKey(UserProfile)

    class Meta:
        #自定义表名
        db_table = 'topic'






