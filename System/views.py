from django.shortcuts import render
from Post import models as pm
from User import models as um
import requests

#决定删掉最新帖子id和最新用户id，因为本身它们在数据库里是自增长的
#并且这个号可能因为删除操作是离散的，无法通过从最新的号倒数几个来获取最新的几个

sendUrl="http://47.106.69.127:10086/send_private_msg?"

#向某个QQ发送信息
def send(QQ,message):
    data=requests.get(sendUrl+"user_id="+str(QQ)+"&message="+message)
    print(data.content)