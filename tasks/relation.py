from .workers import app
from db.dao import SeedidsOper
from page_get import (get_fans_or_followers_ids, get_profile)


@app.task(ignore_result=True)
def crawl_follower_fans(uid):
    user, is_crawled = get_profile(uid)
    if user and user.verify_type == 2:
        SeedidsOper.set_seed_other_crawled(uid)
        return

    rs = get_fans_or_followers_ids(uid, 1, 1)
    rs.extend(get_fans_or_followers_ids(uid, 2, 1))
    datas = set(rs)
    for uid in datas:
        get_profile(uid)
    # If data already exits, just skip it
    # if datas:
    #     SeedidsOper.insert_seeds(datas)
    SeedidsOper.set_seed_other_crawled(uid)


@app.task(ignore_result=True)
def execute_relation_task():
    seeds = SeedidsOper.get_other_ids()
    if seeds:
        for seed in seeds:
            app.send_task('tasks.relation.crawl_follower_fans', args=(seed.uid,), queue='relation_crawler',
                          routing_key='for_relation_info')