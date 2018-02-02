from django.shortcuts import render,redirect
from .models import *
from df_user import user_login
from df_user.models import *
from df_cart.models import *
from django.http import HttpResponse
from django.db import transaction
from datetime import datetime


@user_login.user_decorator_login
def order(request):
    get = request.GET
    # 接收购物车中传过来的id
    items = get.getlist("items")
    if len(items) == 0:
        return redirect('/')
    goods_id_list = [int(x) for x in items]
    # 根据购物表数据id去数据库查找信息
    carts = CartInfo.objects.filter(id__in=goods_id_list)
    user = UserInfo.objects.get(pk=request.session.get('user_id'))
    context = {'title':'提交订单','user':'yes',
               'address':user.uaddress,'receive':user.ureceive,
               'phone':user.uphone,'carts':carts,
               }
    return render(request,'df_order/place_order.html',context)

"""
订单处理，用事务来执行，一旦中间某个环节出现差错，立即回滚：
1.创建订单对象
2.判断库存余量（若不足，rollback）
3.生成订单详情表，保存订单商品内容
4.减少库存，删除购物车表对应内容
5.生成待支付订单
"""

@transaction.atomic()
@user_login.user_decorator_login
def order_handle(request):
    # 创建还原点
    tran_id = transaction.savepoint()
    # 接收购物车内商品
    cart_ids = request.POST.getlist('cart_ids')
    try:
        user_id = request.session.get('user_id')
        order = OrderInfo()
        order.oid = "%s%d"%(datetime.now().strftime('%Y%m%d%H%M%S'),user_id)
        order.user = UserInfo.objects.get(pk=user_id)
        order.odate = datetime.now()
        order.ototal = request.POST.get('total_pay')
        order.save()
        for c in cart_ids:
            cart = CartInfo.objects.get(pk=int(c))
            goods = cart.goods
            if cart.amount <= goods.gstock:
                # 修改商品库存
                goods.gstock -= cart.amount
                goods.save()
                # 创建订单商品详情表
                detail = OrderDetailInfo()
                detail.order = order
                detail.goods = goods
                detail.price = goods.gprice
                detail.count = cart.amount
                detail.save()
                # 删除购物车内对应商品
                cart.delete()
            else:
                # 库存不足
                transaction.savepoint_rollback(tran_id)
                red = redirect('/cart/')
                red.set_cookie('stock', 1)
                return red

        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('--'*10,e)
        transaction.savepoint_rollback(tran_id)
    # 回到用户中心
    return redirect('/user/user_info')


