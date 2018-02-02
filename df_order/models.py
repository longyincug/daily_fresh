from django.db import models

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)
    user = models.ForeignKey('df_user.UserInfo',on_delete=models.CASCADE)
    odate = models.DateTimeField(auto_now=True) # 创建订单时，时间属性值就确定了
    oispay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6,decimal_places=2)


class OrderDetailInfo(models.Model):
    order = models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
    goods = models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
    # 最终的定价可能和商品实际价格不一样，以这个为准
    price = models.DecimalField(max_digits=5,decimal_places=2)
    count = models.IntegerField()



