import requests
import hashlib
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from .models import User
from django.db import connection
import base64

#登录
def logIn(request):
    if(request.method=="POST"):
        uname=request.POST.get("uname")
        password=request.POST.get("password")
        print(uname,password)
        return HttpResponseRedirect("/all/")
    else:
        return render(request, 'User/login.html')


#注册
def register(request):
    #return HttpResponse(models.User.objects.all)

    #登录部分的提交

    """
    数据库
    with connection.cursor() as cursor:
        #使用传参方式，传之前检查防注入攻击
        cursor.execute("select * from User_user where id>%s",[1])
        print(cursor.fetchall())
    """
"""其实不可以放这里，需要与用户的cookie对应！"""
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
        , "Cookie": ""
              }

#教务认证
def check(request):
    if request.method == "POST":
        print("开始提交数据")
        snum = request.POST.get("snum")
        password = request.POST.get("password")
        check=request.POST.get("check")
        print(snum,password,check)

        para = {"j_username": snum,  # 学号改成你的
                "j_password": password,  # 密码改成你的
                "j_captcha": check}
        respon = requests.post("http://202.115.47.141/j_spring_security_check", data=para, headers=header)
        if(respon.url=="http://202.115.47.141/login"):
            print("认证成功！")
        data = requests.get("http://202.115.47.141/index.jsp", headers=header)
        return HttpResponse(data.content)

    else:
        #验证码部分
        cookie= requests.get("http://202.115.47.141/login").headers['Set-Cookie']
        header["Cookie"]=cookie
        print("cookie为"+header["Cookie"])
        img = requests.get("http://202.115.47.141/img/captcha.jpg", headers=header).content
        img=base64.b64encode(img)
        img=str(img,"utf-8")#记得要加上编码，否则显示出错！
        context={'img': img}
        return render(request, 'User/check.html', {"image":context})


"""
数据库操作测试

with connection.cursor() as cursor:
    #使用传参方式，传之前检查防注入攻击
    
    cursor.execute("select userId from User_user")
    print(cursor.fetchall())
    cursor.execute("select * from User_user")
    print(cursor.fetchall())
"""