from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
# 暂时没找到更好的导入其他应用模块的办法
import os
userPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'df_user')
import sys
sys.path.append(userPath)
from df_user import user_login


@ user_login.user_decorator_login
def cart(request):
    user_id = request.session.get('user_id','')
    carts = CartInfo.objects.filter(user=int(user_id))

    context = {'title':'购物车','user':'yes',
                'carts':carts,
               }
    return render(request,'df_cart/cart.html',context)




def cart_handle(request,goods_id,amount):
    goods_id = int(goods_id)
    amount = int(amount)
    user_id = request.session.get('user_id','')
    # 装饰器只适用于全页面刷新，如果这种局部提交，需要另外进行登录验证
    if user_id == '':
        red = redirect('/user/login/')
        # 登录完后要返回之前所在的界面,设置cookie
        red.delete_cookie('pre_path')
        red.set_cookie('pre_path','/'+str(goods_id)+'/')
        return red

    carts = CartInfo.objects.filter(goods=int(goods_id),user=int(user_id))
    if len(carts) >= 1:
        cart = carts[0]
        cart.amount += amount
        cart.save()
        # 这里代表新加入购物车的商品类
        status = 0
    else:
        new_cart = CartInfo()
        new_cart.goods_id = int(goods_id)
        new_cart.user_id = int(user_id)
        new_cart.amount = int(amount)
        new_cart.save()
        # 新加入了一种商品
        status = 1

    if request.is_ajax():
        data = {'status':status}
        return JsonResponse(data)
    return redirect('/cart/')