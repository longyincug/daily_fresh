from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *

from df_user import user_login


@user_login.user_decorator_login
def cart(request):
    user_id = request.session.get('user_id','')
    carts = CartInfo.objects.filter(user=int(user_id))
    # 库存状态码
    stock = request.COOKIES.get('stock','')
    # 将一些运算尽可能交给用户的浏览器去做，减轻服务器的负担
    context = {'title':'购物车','user':'yes',
                'carts':carts,
               'stock':stock,
               }
    ren = render(request, 'df_cart/cart.html', context)
    ren.delete_cookie('stock')
    return ren

# 处理加入购物车的请求
def cart_handle(request,goods_id,amount):
    goods_id = int(goods_id)
    amount = int(amount)
    user_id = request.session.get('user_id','')
    # 装饰器只适用于全页面刷新，如果这种局部提交，需要另外进行登录验证
    # 但ajax不支持重定向！，也就是说，如果用户在未登录情况下点击了加入购物车，需要在模板里另外处理
    if user_id == '':
        red = redirect('/user/login/')
        # 登录完后要返回之前所在的界面,设置cookie
        red.delete_cookie('pre_path')
        red.set_cookie('pre_path','/'+str(goods_id)+'/')
        return red

    carts = CartInfo.objects.filter(goods_id=goods_id,user_id=int(user_id))
    if len(carts) >= 1:
        cart = carts[0]
        cart.amount += amount
        cart.save()
    else:
        new_cart = CartInfo()
        # 注意这里外键的属性字段名要加 下划线id
        new_cart.goods_id = int(goods_id)
        new_cart.user_id = int(user_id)
        new_cart.amount = int(amount)
        new_cart.save()

    if request.is_ajax():
        # 查询该用户购物车中已存在的商品种类数
        amount = CartInfo.objects.filter(user_id=int(user_id)).count()
        data = {'status':amount}
        return JsonResponse(data)
    return redirect('/cart/')


# 处理购物车界面修改数据ajax请求
def edit(request,goods_id,amount):
    goods_id = int(goods_id)
    user_id = request.session.get('user_id')
    cart = CartInfo.objects.filter(user_id=int(user_id), goods_id=goods_id)[0]
    if str(amount).isdigit(): # 数据合法，保存修改
        cart.amount = int(amount)
        cart.save()
        return JsonResponse({'status':1})
    else: # 数据不合法，不保存，返回实际值
        return JsonResponse({'status':0,'amount':cart.amount})


# 处理购物车界面移除商品的ajax请求
def delete(request,goods_id):
    carts = CartInfo.objects.filter(goods_id=int(goods_id))
    if len(carts) == 0:
        return JsonResponse({'status':0})
    else:
        cart = carts[0]
        cart.delete()
        return JsonResponse({'status':1})