from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import Http404
from User.models import User
from .models import Post
from .models import Reply
from .models import ReplyOfPost
from datetime import datetime
from django.db import connection

MAX=20#一页最多显示多少条帖子
Num=len(Post.objects.all())#帖子总数，懒得每次都去查，设为全局变量
sexF={"男":"#3399CC","女":"ff37af","未知":"#aeaeae"}

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
        print(i)
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
            "from (select * from (select replyId_id from Post_replyofpost where postId_id=%s) as ids,Post_reply "
            "where ids.replyId_id=replyId) as temp,User_user "
            "where temp.userId_id=userId "
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
        raise Http404("没有这一页哦")
    pNnum=Num//20#计算总页数
    if(Num%20!=0):
        pNnum+=1
    response[0]["content"]="1\n2 3312\n"
    return render(request, 'Post/all.html', {"data":response,"Pnum":pNnum})


#单独访问某个帖子
def one(request,id):
    post=getPostById(id)
    if(len(post)==0):
        raise Http404("没有这个帖子哦")
    reply=getReply(id)
    return render(request, 'Post/post.html', {"post":post,"reply":reply})