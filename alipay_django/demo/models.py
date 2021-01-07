from django.db import models

# Create your models here.


class Goods(models.Model):
    """商品"""
    goods_name = models.CharField(max_length=100, verbose_name='商品名称')
    goods_price = models.FloatField(default=0.0, verbose_name='商品价格')

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_name


class Order(models.Model):
    """订单信息"""
    ORDER_STATUS = (
        (0, "未支付"),
        (1, "已支付"),
    )

    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品名字')
    order_num = models.CharField(max_length=64, verbose_name='订单序号')
    order_status = models.IntegerField(choices=ORDER_STATUS, default=0)

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}: {}".format(self.goods.goods_name, self.order_num)
