from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
# Create your views here.
import json
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from django.conf import settings
from Crypto.PublicKey import RSA
from rest_framework.response import Response
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64,os,json,time,re
from functools import wraps
from user.models import Version
from user.models import Profile
def localhost(fun):
    @wraps(fun)
    def decorated(*args,**kwargs):
        request=args[1]._request
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ipaddress = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ipaddress = request.META['REMOTE_ADDR']
        print('ip:',ipaddress)
        if not (ipaddress=='localhost' or ipaddress=='127.0.0.1'):
            return HttpResponse("{'code': -1, 'data': 'ip地址不在白名单内'}")
        return fun(*args, **kwargs)
    return decorated

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
import datetime
import urllib.parse
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @action(methods=['get','post'], detail=False)
    def wxcommand(self,request):
        url=request.body.decode()
        print('url:decoee',url)
        url=url.replace('/api/user/wxcommand/?','')
        dic=urllib.parse.parse_qs(url)
        for k in dic:
            dic[k]=dic[k][0]
        print('dic',dic)
        content=dic.get('content','')
        if re.findall(r'绑定',content):
            return self.bindwechat(dic)
        return HttpResponse("服务器出错,未查询到相关指令")

    def bindwechat(self,dic):
        #[消息内容][客户昵称][客户标识]
        #/api/bindwechat/?content=[消息内容]&wechatid=[客户标识]&nickname=[客户昵称]
        nickname=dic.get("nickname", '')
        wechatid=dic.get('wechatid','')
        content=dic.get('content','')
        if not nickname or not wechatid or not content:
            return HttpResponse("服务器出错,请联系管理员")
        if (tmp:=re.findall(r'(\d+)',content)):
            id=tmp[0]
            try:
                u=User.objects.get(id=id)
                if  u.profile.wechatid:
                    return HttpResponse("该账号已绑定过微信")
            except Exception as e:
                return HttpResponse("未查询到用户,请联系管理员")
            try:
                tmpp=Profile.objects.filter(wechatid=wechatid).first()
                if tmpp:
                    return HttpResponse("绑定失败,该微信账号已绑定过")
            except Exception as e:
                pass
            u.profile.wechatid=wechatid
            u.profile.wechatnickname=nickname
            u.profile.tulongtryflag=True
            if u.profile.tulong_endtime and u.profile.tulong_endtime > datetime.datetime.now():
                u.profile.tulong_endtime = u.profile.tulong_endtime + datetime.timedelta(days=1)
            else:
                u.profile.tulong_endtime = datetime.datetime.now() + datetime.timedelta(days=1)
            u.profile.save()
            return HttpResponse("绑定成功!")
        else:
            return HttpResponse("请输入正确的绑定信息")
    @action(methods=['get','post'], detail=False)
    def getversion(self,request):
        version=request.query_params.get('version','fengchuan')
        print('version:',version)
        model=Version.objects.filter(username=version).first()
        if model:
            ret={'username':model.username,'qq':model.qq,'wechaturl':model.wechaturl}
            print('ret:',ret)
            ret=json.dumps(ret)
            return HttpResponse(ret)
        else:
            ret={'username': '请联系管理员', 'qq': '请联系管理员', 'wechaturl':'请联系管理员'}
            ret = json.dumps(ret)
            return HttpResponse(ret)
    @action(methods=['get'], detail=False)
    def getuserinfo(self,request):
        if not request.user.is_authenticated:
            return HttpResponse("{'code':-1,'username':'请先登录'}")
        ret={"username":request.user.username,"code":"0",
             "wechatid":request.user.profile.wechatid,
             "wechatnickname":request.user.profile.wechatnickname,
             "tulong_endtime":request.user.profile.tulong_endtime.strftime('%Y-%m-%d %H:%M:%S') if request.user.profile.tulong_endtime else '',
             "remotetime":int(time.time()),
             "tulongtryflag":request.user.profile.tulongtryflag,
             "tulong_enabled": 1 if request.user.profile.tulong_endtime and request.user.profile.tulong_endtime > datetime.datetime.now() else 0,
             "id":request.user.id,
             }
        if settings.DEBUG:
            return HttpResponse(json.dumps(ret))
        else:
            try:
                rsakey = RSA.importKey(open(os.path.join(settings.BASE_DIR,"rsa_public_key.pem")).read())
                cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
                ENCLEN = 117
                content=json.dumps(ret).encode()
                contentlen = len(content)
                p = 0
                b = []
                while p < contentlen:
                    cipher_text = cipher.encrypt(content[p:p + ENCLEN])
                    b.append(cipher_text)
                    p += ENCLEN


                cipher_text = base64.b64encode(b''.join(b))
            except Exception as e:
                print(e)
            print('cipher',cipher_text)
            return HttpResponse(cipher_text)

    @action(methods=['get'], detail=False)
    def register(self,request):
        username=request.query_params.get('username', '')
        password=request.query_params.get('password', '')
        if not password:
            return HttpResponse('{"code":-1,"msg":"密码不能为空"}')
        if not username:
            return HttpResponse('{"code":-1,"msg":"用户名不能为空"}')
        u=User.objects.filter(username=username).first()
        if u:
            return HttpResponse('{"code":-1,"msg":"用户名已存在"}')
        u=User()
        u.username=username
        u.set_password(request.query_params.get('password', ''))

        u.save()
        u.profile.tulong_endtime=datetime.datetime.now()+datetime.timedelta(days=7)
        u.profile.tulongtryflag=1
        u.profile.save()
        return HttpResponse('{"code":0,"msg":"注册成功"}')
    @localhost
    @action(methods=['get'], detail=False)
    def getuserinfo_debug(self,request):

        ret={"username":request.user.username,"code":"0",
             "wechatid":request.user.profile.wechatid,
             "wechatnickname":request.user.profile.wechatnickname,
             "tulong_endtime":request.user.profile.tulong_endtime.strftime('%Y-%m-%d %H:%M:%S'),
             "tulong_enabled":1 if request.user.profile.tulong_endtime and request.user.profile.tulong_endtime>datetime.datetime.now() else 0,
             "remotetime":int(time.time()),
             "tulongtryflag":request.user.profile.tulongtryflag,
            "tulong_accout_numlimit":request.user.profile.tulong_accout_numlimit,
             "id": request.user.id,
             }
        return HttpResponse(json.dumps(ret))