from django.shortcuts import render
from .models import *
from django.core import paginator
from df_cart import models
# Create your views here.

def index(request):
    typelist = TypeInfo.objects.all()
    # 按id降序排列，取最新的四个商品
    # 按点击量降序排序，取最火的四个商品
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    # 查询该用户购物车的商品类数量
    amount = models.CartInfo.objects.filter(user_id=int(request.session.get('user_id', 0))).count()
    context = {'title':'首页','goods':'yes',
               'type0':type0,'type01':type01,
               'type1':type1,'type11':type11,
               'type2':type2,'type21':type21,
               'type3':type3,'type31':type31,
               'type4':type4,'type41':type41,
               'type5':type5,'type51':type51,
               'status':amount,
               }
    return render(request, 'df_goods/index.html', context)

def list_handle(request,type,page,sort):
    # type 商品的类别
    # sort 商品排序的依据 1为默认，2为价格，3为点击量
    # page 商品列表的页码，每页10条数据
    goodslist = GoodsInfo.objects.filter(gtype=type)
    sort = int(sort)
    page = int(page)
    if sort == 1:
        goodslist = goodslist
    elif sort == 2:
        goodslist = goodslist.order_by('gprice')
    elif sort == 3:
        goodslist = goodslist.order_by('-gclick')

    # 新品推荐的两个商品
    newlist = goodslist.order_by('-id')[0:2]
    # 商品列表页的10个商品
    pagi = paginator.Paginator(goodslist, 10)
    pagelist = pagi.page(page)
    # 查询该用户购物车的商品类数量
    amount = models.CartInfo.objects.filter(user_id=request.session.get('user_id', '')).count()
    context = {'title':'商品列表','goods':'yes',
               'sort':sort,
               'pagelist':pagelist,
               'new':newlist,
               'page':page,
               'type':type,
               'status':amount,
               }
    return render(request, 'df_goods/list.html', context)

def detail(request, id):
    goods = GoodsInfo.objects.filter(pk=int(id))[0]
    goods.gclick += 1
    goods.save()
    new_list = GoodsInfo.objects.filter(gtype=goods.gtype).order_by('-id')[0:2]
    # 判断用户有没有登录，以便在用户点击加入购物车时，做出正确的反应
    uid = request.session.has_key('user_id')
    # 查询该用户购物车的商品类数量
    amount = models.CartInfo.objects.filter(user_id=request.session.get('user_id','')).count()
    context = {'title': "商品详情", 'goods': 'yes',
               'new': new_list,
               'g': goods,
               'goods_id': id,
               'uid': uid,
               'status': amount,
               }
    res = render(request, 'df_goods/detail.html', context)

    if request.session.has_key('user_id'):
        # 最近浏览5个商品需要存到cookie中,（前提是登录了）
        goods_id = '%d'%goods.id
        cookieStr = request.COOKIES.get('ago','')
        # 第一次为空，不能split，否则会产生一个空字符串
        cookieList = []
        if cookieStr != '':
            cookieList = cookieStr.split(',')
            # print(cookieList,"--"*20)
            if goods_id in cookieList:
                cookieList.remove(goods_id)
        cookieList.insert(0,goods_id)
        if len(cookieList) > 5:
            del cookieList[5]
        # 将最近浏览商品的id以字符串形式存储到cookie中
        cookieStr = ','.join(cookieList)
        res.set_cookie('ago', cookieStr)
    return res


# 搜索框，自定义上下文,传递到模板中
from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super().extra_context()
        context['title'] = '搜索'
        context['goods'] = 'yes'
        context['status'] = models.CartInfo.objects.filter(user_id=self.request.session.get('user_id', '')).count()
        return context
