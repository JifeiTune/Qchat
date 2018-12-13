from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from User.models import User
from .models import Post
from .models import Reply
from datetime import datetime
from django.db import connection
import time
import requests
from System.views import send

MAX=20#一页最多显示多少条帖子
Num=len(Post.objects.all())#帖子总数，懒得每次都去查，设为全局变量
sexF={"男":"#3399CC","女":"#ff37af","未知":"#aeaeae"}

#一个帖子所需字典数据
def postDic(uname,sex,crtime,head,content,prNum,ctrNum,repNum,postId):
    date=datetime.fromtimestamp(crtime).__str__()
    #因为目前性别通过颜色来判断，所以暂时把性别替换成颜色字符串
    sex=sexF[sex]
    return {"uname":uname,"sex":sex,"crtime":date,"head":head,"content":content,"prNum":prNum,"ctrNum":ctrNum,"repNum":repNum,"postId":postId}

#一个回复所需的字典数据
def replyDic(uname,sex,crtime,content,prNum,ctrNum):
    date=datetime.fromtimestamp(crtime).__str__()
    return {"uname":uname,"sex":sex,"crtime":date,"content":content,"prNum":prNum,"ctrNum":ctrNum}

#取得按发布时间降序排序时，[be,ed]的帖子信息列表，
def getPostByOrder(be,ed):
    be-=1#因为实际上下标从0开始
    response = []
    with connection.cursor() as cursor:
        cursor.execute(
            "select uname,sex,crtime,head,content,prNum,ctrNum,repNum,postId "
            "from Post_post,User_user where userId_id=userId "
            "order by crTime desc "
            "limit %s offset %s",[ed-be,be])
        data = cursor.fetchall()
    for i in data:
        response.append(postDic(*i))
        #print(response)
    return response

#根据帖子id获取帖子信息
def getPostById(id):
    with connection.cursor() as cursor:
        cursor.execute(
            "select uname,sex,crtime,head,content,prNum,ctrNum,repNum,postId "
            "from Post_post,User_user where userId_id=userId and postId=%s"
            ,[id])
        data = cursor.fetchall()
    response=postDic(*data[0])
    return response

#返回某一页，用于分页展示
def getPage(id):
    id=int(id)
    if(id<1):
        id=1
    if((id-1)*MAX>=Num):
        return []
    return getPostByOrder((id-1)*MAX,id*MAX)

#返回某个帖子的所有回复（目前只是回复楼主，今后做成可以回复回复）
def getReply(id):
    with connection.cursor() as cursor:
        cursor.execute(
            "select uname,sex,crtime,content,prNum,ctrNum  "
            "from (select * from Post_reply where postId_id=%s) "
            "as reply,User_user where reply.userId_id=userId"
            ,[id])
        data = cursor.fetchall()
    response=[]
    for i in data:
        response.append(replyDic(*i))
    return response

#直接访问是主页，get参数可指定页数
def all(request):
    id=request.GET.get("page")
    if(id==None):
        id=1
    response=getPage(id)
    if(len(response)==0):
        return HttpResponse("没有这一页哦")
    pNnum=Num//20#计算总页数
    if(Num%20!=0):
        pNnum+=1

    info={"Pnum":pNnum,"uname":"登录"}
    #判断登录状态
    uname=request.session.get("uname")
    if(uname!=None):
        info["uname"]=uname
    #我的天，一直以为session模块不工作，调了半天bug，原来只有你用上了它，才会去set-cookie
    return render(request, 'Post/all.html', {"data":response,"info":info})


#单独访问某个帖子与回复帖子
def one(request,id):
    uname=request.session.get("uname")
    if(request.method=="POST"):
        if(uname==None):
            return HttpResponseRedirect("/user/login")#未登录则跳转
        #回复内容写入数据库
        content=request.POST.get("content")
        uid=request.session.get("uid")#发送者id
        pobj=Post.objects.get(postId=id)#回复的帖子
        uobj=User.objects.get(userId=uid)#发送者
        ruobj=User.objects.get(userId=pobj.userId.userId)#接收者，注意查找外键返回的还是个对象，不是实际内容
        robj=Reply(userId=uobj,revId=ruobj,crTime=int(time.time()),content=content,postId=pobj)
        robj.save()
        #帖子与回复的映射写入数据库
        pobj.repNum+=1#回复数要+1
        pobj.save()
        #好了，接下来要使用QQ机器人发送一条回复
        QQ=ruobj.QQ
        message="小主的帖子有新回复了哦！\n" \
                "回复人：%s\n" \
                "回复内容：%s\n" \
                "快去看看吧！\n" \
                "http://127.0.0.1:8000/all/%s" % (uobj.uname,content,id)
        send(QQ,message)#向接收者QQ发送数据

    post=getPostById(id)
    if(len(post)==0):
        return HttpResponse("没有这个帖子哦")
    reply=getReply(id)
    info={"uname":"登录"}
    #判断登录状态
    if(uname!=None):
        info["uname"]=uname
    return render(request, 'Post/post.html', {"post":post,"reply":reply,"info":info})

#发布帖子
def creat(request):
    uname=request.session.get("uname")
    uid=request.session.get("uid")
    #判断登录状态
    if(uname==None):
        return HttpResponseRedirect("/user/login/")
    if(request.method=="POST"):
        head=request.POST.get("head")
        content=request.POST.get("content")
        if(head==""):
            return HttpResponse("标题不能为空！")
        crtime=int(time.time())
        obj=User.objects.get(userId=uid)#外键原因，要这样写
        Post.objects.create(userId=obj,crTime=crtime,head=head,content=content)
        return HttpResponseRedirect("../")#发帖成功后跳转到主页
    else:
        info={"uname":"登录"}
        if(uname!=None):
            info["uname"]=uname
        return render(request, 'Post/new.html',{"info":info})