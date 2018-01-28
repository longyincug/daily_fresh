from django.shortcuts import render
from .models import *
from django.core import paginator
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
    context = {'title':'首页','goods':'yes',
               'type0':type0,'type01':type01,
               'type1':type1,'type11':type11,
               'type2':type2,'type21':type21,
               'type3':type3,'type31':type31,
               'type4':type4,'type41':type41,
               'type5':type5,'type51':type51,

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
    context = {'title':'商品列表','goods':'yes',
               'sort':sort,
               'pagelist':pagelist,
               'new':newlist,
               'page':page,
               'type':type,
               }
    return render(request, 'df_goods/list.html', context)

def detail(request, id):
    goods = GoodsInfo.objects.filter(pk=int(id))[0]
    goods.gclick += 1
    goods.save()
    new_list = GoodsInfo.objects.filter(gtype=goods.gtype).order_by('-id')[0:2]

    context = {'title':"商品详情",'goods':'yes',
               'new':new_list,
                'g':goods,
               }
    return render(request, 'df_goods/detail.html',context)