from django.db import models

# Create your models here.
class Order(models.Model):
    ordernum=models.CharField(verbose_name='订单号',max_length=128,db_index=True)
    money=models.FloatField(verbose_name='金额',default=0)
    nickname=models.CharField(verbose_name='昵称',max_length=32)
    product=models.CharField(verbose_name='产品',max_length=32,db_index=True)
    num=models.IntegerField(verbose_name='数量',default=0)
    wechatid=models.TextField(verbose_name='买家标识',default='')
    time=models.DateTimeField(verbose_name='时间',blank=True,null=True,db_index=True)
    finished=models.BooleanField(verbose_name='完成',blank=True,null=True,default=False)