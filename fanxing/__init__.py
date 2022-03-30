import pymysql
pymysql.install_as_MySQLdb()
import shutil
import re
from django.conf import settings
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64,os,json
if os.path.exists(os.path.join(settings.BASE_DIR,"static","js")):
    files=os.listdir(os.path.join(settings.BASE_DIR,"static","js"))
else:
    files=[]
if settings.DEBUG==True:
    rsakey = RSA.importKey(open(os.path.join(settings.BASE_DIR, "rsa_public_key.pem")).read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    ENCLEN=117
    for f in files:
        if f.endswith('.map'):
            os.remove(os.path.join(settings.BASE_DIR,"static","js",f))


        if f.endswith(".js") and not os.path.exists(os.path.join(settings.BASE_DIR,"static","js",f+".old")):
            shutil.copyfile(os.path.join(settings.BASE_DIR,"static","js",f),os.path.join(settings.BASE_DIR,"static","js",f+".old"))
            with open(os.path.join(settings.BASE_DIR,"static","js",f),'rb+') as f:

                content=f.read()
                f.seek(0)
                f.truncate()
                contentlen=len(content)
                p=0
                b=[]
                while p<contentlen:
                    cipher_text = cipher.encrypt(content[p:p+ENCLEN])
                    b.append(cipher_text)
                    p+=ENCLEN
                f.write(b''.join(b))


from django.conf import settings
if os.path.exists(r'C:\Users\fengchuan\GolandProjects\fanxing\main.go'):
    with open(r'C:\Users\fengchuan\GolandProjects\fanxing\main.go','r+',encoding='utf8') as f:
        content=f.read()
        if settings.DEBUG==False:
            if re.findall(r'var Rsascript = false',content):
                content=content.replace(r'var Rsascript = false',r'var Rsascript = true')
        else:
            if re.findall(r'var Rsascript = true', content):
                content = content.replace( r'var Rsascript = true',r'var Rsascript = false')
        f.seek(0)
        f.write(content)

