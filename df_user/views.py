from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from hashlib import sha1
import os
goodsPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'df_goods')
import sys
sys.path.append(goodsPath)
# print(sys.path)
from df_goods import models # 如何导入另一个应用的模型类，也需要注意


def df_register(request):
    context = {'title':'用户注册'}
    return render(request, 'df_user/register.html', context)


def df_register_handle(request):
    post = request.POST
    if post.get('pwd') != post.get('cpwd'):
        return  redirect('/user/register')
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
    uname = request.COOKIES.get('uname', '')
    context = {'title':'用户登录','uname':uname}
    return render(request, 'df_user/login.html', context)

def df_login_handle(request):
    post = request.POST
    uname = post.get('username')
    pwd = post.get('pwd')
    remember = post.get('remember')

    userlist = UserInfo.objects.filter(uname=uname)
    if len(userlist) == 1:
        user = userlist[0]
        s1 = sha1()
        s1.update(pwd.encode('utf-8'))
        pwd2 = s1.hexdigest()
        if pwd2 == user.upwd:
            # 判断，如果用户是在浏览中途登录的，登录后切换回去
            url = request.COOKIES.get('pre_path','/')
            # 提前构造一个返回对象，是为了给其添加cookie
            red = HttpResponseRedirect(url)
            # 删除之前访问的url cookie
            red.delete_cookie('pre_path')
            if remember == 'yes':
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = user.id
            request.session['user_name'] = uname
            # context = {'uname':uname,'uemail':uemail,'uaddress':uaddress}
            # 这里不适合直接渲染网页内容，应该重定向一个URL，那么数据怎么传递呢？使用session！
            # return render(request, 'df_user/user_center_info.html',context)
            return red

        else:
            context = {'title':'用户登录'}
            return render(request,'df_user/login.html',context)
    else:
        context = {'title':'用户登录'}
        return render(request,'df_user/login.html',context)

def df_logout(request):
    # request.session.flush()
    # 用户退出时，别清空所有session，否则历史浏览等数据就不存在了
    del request.session['user_id']
    del request.session['user_name']
    return redirect('/')

from .user_login import *
# 用装饰器，进行登录验证
@user_decorator_login
def user_info(request):
    user_email = UserInfo.objects.get(id = request.session['user_id']).uemail
    user_address = UserInfo.objects.get(id = request.session['user_id']).uaddress
    # 从cookie中取出用户最近浏览商品的id字符串
    agoGoodsIDs = request.COOKIES.get('ago','')
    # 为防止没有浏览记录的用户报错
    if agoGoodsIDs == '':
        goodsList = []
    else:
        # 将最近浏览商品id字符串转化为商品对象列表
        idList = agoGoodsIDs.split(',')
        # print(idList, "-" * 30)
        goodsList = []
        for g in idList:
            goods = models.GoodsInfo.objects.get(pk=int(g))
            goodsList.append(goods)

    context = {'user':'yes','title':'用户中心','uname':request.session['user_name'],
               'uemail':user_email,'uaddress':user_address,
               'goodsList':goodsList,
               }
    return render(request, 'df_user/user_center_info.html',context)

@user_decorator_login
def user_site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    receive = user.ureceive
    address = user.uaddress
    post = user.upost
    phone = user.uphone
    context = {'user':'yes','title':'用户中心','receive':receive,'address':address,'post':post,'phone':phone}
    return render(request, 'df_user/user_center_site.html', context)

def site_handle(request):
    post = request.POST
    user = UserInfo.objects.get(id=request.session['user_id'])
    user.ureceive = post.get('receive','')
    user.uaddress = post.get('address','')
    user.upost = post.get('post','')
    user.uphone = post.get('phone','')
    user.save()
    return redirect('/user/user_site')

@user_decorator_login
def user_order(request):
    context = {'title':'用户中心','user':'yes'}
    return render(request, 'df_user/user_center_order.html',context)



