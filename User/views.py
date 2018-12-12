import requests
import hashlib
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from .models import User
from django.http import Http404
from django.db import connection
import base64

def hash(string):
    string=string.encode(encoding='UTF-8')
    return hashlib.md5(string).hexdigest()

#登录
def logIn(request):
    if(request.method=="POST"):
        uname=request.POST.get("uname")
        password=request.POST.get("password")
        password=hash(password)
        if(uname=="" or password==""):
            return HttpResponse("用户名或密码为空！")
        with connection.cursor() as cursor:
            cursor.execute("select password,userId from User_user where uname=%s",[uname])
            ans=cursor.fetchall()
        if(len(ans)==0):
            return HttpResponse("用户不存在！")
        elif(password!=ans[0][0]):
            return HttpResponse("密码错误！")
        else:
            request.session["uname"]=uname#登录成功，记录进session
            request.session["uid"]=ans[0][1]
            return HttpResponseRedirect("/all/")
    else:
        return render(request, 'User/login.html')


#注册
def register(request):
    if(request.method=="POST"):
        uname=request.POST.get("uname")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        if(password1!=password2):
            return HttpResponse("两次密码不一致！")
        if(len(User.objects.filter(uname=uname))):
            return HttpResponse("用户名已存在！")
        password1=hash(password1)#存hash
        uobj=User(uname=uname,password=password1)
        uobj.save()
        request.session["uid"]=uobj.userId
        request.session["uname"]=uname
        return HttpResponseRedirect("/all")

    else:
        return render(request,'User/resister.html')
    #登录部分的提交



#找回密码
def forget(request):
    if(request.method=="POST"):
        return HttpResponse("1")
    else:
        return render(request,'User/forget.html')


#教务认证
def check(request):
    uid=request.session.get("uid")
    if(uid==None):#若未登录，跳转到登录界面
        return HttpResponseRedirect("../login/")
    uobj=User.objects.get(userId=uid)
    if(uobj.checked):#先检查是否已经通过了教务认证
        return HttpResponse("您已经通过教务认证了哦！")
    if request.method == "POST":
        print("开始提交数据")
        snum = request.POST.get("snum")
        password = request.POST.get("password")
        check=request.POST.get("check")
        header={"Cookie": request.session.get("yzm")}
        para = {"j_username": snum,  # 学号改成你的
                "j_password": password,  # 密码改成你的
                "j_captcha": check}
        respon = requests.post("http://202.115.47.141/j_spring_security_check", data=para, headers=header)
        if(respon.url=="http://202.115.47.141/login"):
            uobj.checked=True
            uobj.snum=snum
            uobj.save()
            return HttpResponseRedirect("../set")
        else:
            return HttpResponse("认证失败！学号或密码或验证码错误！")
        """
        data = requests.get("http://202.115.47.141/index.jsp", headers=header)
        return HttpResponse(data.content)
        """
    else:
        #验证码部分
        header={"Cookie": ""}
        cookie= requests.get("http://202.115.47.141/login").headers['Set-Cookie']
        request.session["yzm"]=cookie#把这个教务处cookie记录进session
        header["Cookie"]=cookie
        img = requests.get("http://202.115.47.141/img/captcha.jpg", headers=header).content
        img=base64.b64encode(img)
        img=str(img,"utf-8")#记得要加上编码，否则显示出错！
        context={'img': img}
        return render(request, 'User/check.html', {"image":context})

#修改个人信息
def set(request):
    uid=request.session.get("uid")
    uname=request.session.get("uname")
    if(uid==None):#若未登录，跳转到登录界面
        return HttpResponseRedirect("../login/")
    else:
        uobj=User.objects.get(userId=uid)
        if(request.method=="POST"):
            QQ=request.POST.get("QQ")
            sex=request.POST.get("sex")
            if(uobj.QQ!=QQ):
                uobj.QQ=QQ
                uobj.save()
            if(uobj.sex!=sex):
                uobj.sex=sex
                uobj.save()
            return HttpResponseRedirect("./")
        else:
            uobj=User.objects.get(userId=uid)
            snum="暂未设置"
            QQ=""
            checked=""
            select={"man":"","woman":"","unknown":""}
            trans={"男":"man","女":"woman","未知":"unknown"}
            select[trans[uobj.sex]]='selected="selected"'
            checkDisplay="unset"
            if(uobj.snum!=0):
                snum=uobj.snum
            if(uobj.QQ!=0):
                QQ=uobj.QQ
            if(uobj.checked):
                checked="checked"
                checkDisplay="none"
            data={"uname":uname,"snum":snum,"QQ":QQ,"checked":checked,"checkDisplay":checkDisplay}
            data.update(select)
            return render(request,'User/set.html',{"data":data})

#退出登录
def logOut(request):
    del request.session["uid"]
    del request.session["uname"]
    return HttpResponseRedirect("/all")

#修改密码
def reset(request):
    if(request.method=="POST"):
        return HttpResponse("1")
    else:
        return render(request,'User/reset.html')