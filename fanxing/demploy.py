import sys
import django
import os,re
import pathlib,shutil
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64,os,json
with open('settings.py','r',encoding='utf8') as f:
    content=f.read()
    domain=re.findall(r'DOMAIN=.*?"(.*?)"',content)[0]
    print('domain:',domain)
domainurl=f'var Domain = "{domain}"'
print(domainurl)

with open(r'C:\Users\fengchuan\GolandProjects\fanxing\main.go', 'r+', encoding='utf8') as f:
    content = f.read()
    if not re.findall(domainurl,content):
        t1=re.findall(r'var Domain = ".*?"',content)[0]
        content=content.replace(t1,domainurl)

    if re.findall(r'var Rsascript = false', content):
        content = content.replace(r'var Rsascript = false', r'var Rsascript = true')
    f.seek(0)
    f.truncate()
    f.write(content)

os.chdir(r'F:\Users\fengchuan\WebstormProjects\fanxing')
os.system("npm run build")

os.chdir(r'F:\Users\fengchuan\PycharmProjects\fanxing')
BASE_DIR=r'F:\Users\fengchuan\PycharmProjects\fanxing'
files=os.listdir(os.path.join(BASE_DIR,"static","js"))

if 1:
    rsakey = RSA.importKey(open(os.path.join(BASE_DIR, "rsa_public_key.pem")).read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    ENCLEN=117
    for f in files:
        if f.endswith('.map'):
            os.remove(os.path.join(BASE_DIR,"static","js",f))


        if f.endswith(".js") and not os.path.exists(os.path.join(BASE_DIR,"static","js",f+".old")):
            shutil.copyfile(os.path.join(BASE_DIR,"static","js",f),os.path.join(BASE_DIR,"static","js",f+".old"))
            with open(os.path.join(BASE_DIR,"static","js",f),'rb+') as f:

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

if __name__ == "__main__":
    basedir = str(pathlib.Path(__file__).resolve().parent.parent)
    os.chdir(basedir)
    sys.path.append(basedir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'fanxing.settings'
    os.environ['DEBUG']="0"
    django.setup()

from django.conf import settings
from user.models import Version

os.chdir(r'C:\Users\fengchuan\GolandProjects\fanxing')
models=Version.objects.all()
for model in models:
    dir=os.path.join(r'C:\Users\fengchuan\GolandProjects\fanxing\dist',model.username)
    print('dir:',dir)
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(r'C:\Users\fengchuan\GolandProjects\fanxing\main.go', 'r+', encoding='utf8') as f:
        content = f.read()
        v1= re.findall(r'var Version = ".*?"', content)[0]
        content = content.replace(v1, f'var Version = "{model.username}"')
        f.seek(0)
        f.truncate()
        f.write(content)
    os.system(f'go build -o {dir}\\繁星屠龙助手.exe -ldflags "-extld=gcc -extldflags=resources.syso -H=windowsgui -s -w" main.go')
