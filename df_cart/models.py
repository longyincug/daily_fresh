from django.db import models

# Create your models here.

class CartInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
    user = models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE)
    amount = models.IntegerField()