from django.shortcuts import render
from Post import models as pm
from User import models as um

#决定删掉最新帖子id和最新用户id，因为本身它们在数据库里是自增长的
#并且这个号可能因为删除操作是离散的，无法通过从最新的号倒数几个来获取最新的几个

"""
保存与删除
obj=um.User(snum="4",QQ=4)
obj.save()

obj.delete()
"""
