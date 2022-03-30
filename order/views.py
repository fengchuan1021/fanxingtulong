import datetime

from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from order.models import Order
# Create your views here.
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from django.conf import settings
from user.models import Profile
import base64,os,json
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ='__all__'
import urllib.parse
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(methods=['get','post'], detail=False)
    def chargeforuser(self,request):
        url=request.body.decode()
        url=url.replace('/api/order/chargeforuser/?','')
        dic=urllib.parse.parse_qs(url)
        for k in dic:
            dic[k]=dic[k][0]
        try:
            #/api/chargeforuser/?nickname=[买家昵称]&wechatid=[买家标识]&product=[产品名]&money=[购买金额]
            order=Order()
            order.nickname=dic.get("nickname",'')
            order.money = dic.get("money", 0)
            order.product=dic.get("product", '')
            order.wechatid=request.query_params.get("wechatid", '')
            order.time=datetime.datetime.now()

            if order.product == '繁星屠龙助手':
                print("屠龙助手")
                p=Profile.objects.filter(wechatid=order.wechatid).first()
                if not p:
                    order.finished=0
                    order.save()
                    return HttpResponse("未查询到用户信息,请联系管理员")
                if p.tulong_endtime and p.tulong_endtime>datetime.datetime.now():
                    p.tulong_endtime=p.tulong_endtime+datetime.timedelta(days=31)
                    order.finished=1
                else:
                    order.finished = 1
                    p.tulong_endtime=datetime.datetime.now()+datetime.timedelta(days=31)
                p.save()
                order.save()
                return HttpResponse("充值成功,请刷新信息")
            order.save()
            return HttpResponse("充值成功")
        except Exception as e:
            print(e)
            return HttpResponse("充值失败请联系管理员")
