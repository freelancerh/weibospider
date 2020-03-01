# coding:utf-8
from tasks import workers

#需要加上启动参数
# -A tasks.workers -Q login_queue,user_crawler,fans_followers,search_crawler,home_crawler worker -l info -c 1
# windows系统还要加上 --pool=solo
if __name__ == '__main__':
    workers.app.start()