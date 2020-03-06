FROM python:3.5

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
CMD ["celery", "-A", "tasks.workers", "worker", "-l", "info", "-c", "1"]
