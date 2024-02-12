FROM python:3.9

WORKDIR /project

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor
RUN apt-get install -y ffmpeg
RUN pip3 install uwsgi

COPY requirements.txt requirements.txt

RUN pip3 install -r /project/requirements.txt


RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY server-conf/nginx.conf /etc/nginx/
COPY server-conf/flask-site-nginx.conf /etc/nginx/conf.d/
COPY server-conf/uwsgi.ini /etc/uwsgi/
COPY server-conf/supervisord.conf /etc/supervisor/

COPY . .



CMD ["/usr/bin/supervisord"]
