from django.db import models
from tinymce.models import HTMLField # 富文本编辑器，别忘了注册应用，添加根级URL

# Create your models here.
class TypeInfo(models.Model):
    # id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='goods_pics')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20,default='500g')
    gclick = models.IntegerField(default=0)
    gdesc = models.CharField(max_length=100) # 商品简介
    gstock = models.IntegerField() # 商品库存
    gcontent = HTMLField() # 商品详情
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.gtitle