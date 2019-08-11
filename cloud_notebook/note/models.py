from django.db import models
from user.models import User



# Create your models here.
class Note(models.Model):
    title = models.CharField("标题",max_length=100,default='')
    content = models.TextField("内容",default='',max_length=1000)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)
    mod_time = models.DateTimeField("修改时间",auto_now=True)
    author = models.ForeignKey(User)
