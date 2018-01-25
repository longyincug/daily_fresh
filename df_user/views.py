from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from hashlib import sha1

# Create your views here.

def df_register(request):
    return render(request, 'df_user/register.html')


def df_register_handle(request):
    post = request.POST
    if post.get('pwd') != post.get('cpwd'):
        return  redirect('/user/registerHandle')
    user = UserInfo()
    user.uname = post.get('user_name')
    pwd = post.get('pwd')
    # 密码加密
    s1 = sha1()
    s1.update(pwd.encode('utf-8'))
    pwd2 = s1.hexdigest()
    user.upwd = pwd2
    user.uemail = post.get('email')
    user.save()
    # 注册成功，重定向到登陆界面
    return render(request, 'df_user/login.html')

def df_login(request):
    pass
