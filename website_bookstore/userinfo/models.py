from django.db import models

# Create your models here.

# userinfo/models.py

class User(models.Model):
    name = models.CharField('用户名', max_length=30,
                            unique=True)
    password = models.CharField('密码', max_length=30)

    def __str__(self):
        return "用户" + self.name

