FROM python:3.9
#COPY . /app
WORKDIR /fanxing
ENV DEBIAN_FRONTEND noninteractive
RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  apt-get clean
RUN apt-get update
RUN apt install -y cron
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
COPY ./requirements.txt /fanxing/requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn uvicorn

RUN sed  -i -e '546c \            sql = sql.encode(self.encoding,"backslashreplace")'   /usr/local/lib/python3.9/site-packages/pymysql/connections.py

CMD cron start && python3 manage.py  crontab add  \
&& gunicorn fanxing.asgi:application -p /fanxing/run/gunicorn.pid -b 0.0.0.0:8000 -w 8 -k uvicorn.workers.UvicornWorker --log-file -



