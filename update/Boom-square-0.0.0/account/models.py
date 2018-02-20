from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    timedate = models.TimeField()
    '''
    auth_now 更新时间
    auth_now_add 创建时间
    '''
    # timedate = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.username
