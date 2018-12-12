from django.db import models

# Create your models here.
class User(models.Model):
    AllSex = (("男", "男性"), ("女", "女性"), ("未知", "性别未知"),)

    #userId，几乎所有用户相关表的主键
    userId=models.AutoField(primary_key=True)
    #用户名
    uname=models.CharField(max_length=10)
    #密码hash
    password=models.CharField(max_length=32)
    #学号
    snum=models.IntegerField(default=0)
    #是否通过教务认证
    checked=models.BooleanField(default=False)
    #绑定的QQ
    QQ=models.IntegerField(default=0)
    #性别
    sex=models.CharField(max_length=2,choices=AllSex,default="未知")
    #禁言恢复时间(UNIX)
    recTime=models.IntegerField(default=0)
    #已被禁言次数
    fobNum=models.IntegerField(default=0)


    def __str__(self):
        return 'User: '+self.uname

