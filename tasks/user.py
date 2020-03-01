from .workers import app
from db.dao import SeedidsOper
from page_get import (get_fans_or_followers_ids, get_profile, get_user_profile,
                      get_newcard_by_name)
from logger import crawler
from celery.exceptions import SoftTimeLimitExceeded


@app.task(ignore_result=True)
def crawl_person_infos(uid):
    """
    Crawl user info and their fans and followers
    For the limit of weibo's backend, we can only crawl 5 pages of the fans and followers.
    We also have no permissions to view enterprise's followers and fans info
    :param uid: current user id
    :return: None
    """
    if not uid:
        return

    try:
        user, is_crawled = get_profile(uid)

    # By adding '--soft-time-limit secs' when you start celery, this will resend task to broker
    # e.g. celery -A tasks.workers -Q user_crawler worker -l info -c 1 --soft-time-limit 10
    except SoftTimeLimitExceeded:
        crawler.error("user SoftTimeLimitExceeded    uid={uid}".format(uid=uid))
        app.send_task('tasks.user.crawl_person_infos', args=(uid, ), queue='user_crawler',
                      routing_key='for_user_info')


@app.task(ignore_result=True)
def crawl_person_infos_not_in_seed_ids(uid):
    """
    Crawl user info not in seed_ids
    """
    if not uid:
        return

    get_user_profile(uid)


def crawl_person_infos_by_name(name):
    """
    Crawl user info by name
    """
    if not name:
        return False

    user, is_crawled = get_newcard_by_name(name)


@app.task(ignore_result=True)
def execute_user_task():
    seeds = SeedidsOper.get_seed_ids()
    if seeds:
        for seed in seeds:
            app.send_task('tasks.user.crawl_person_infos', args=(seed.uid,), queue='user_crawler',
                          routing_key='for_user_info')
