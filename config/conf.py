import os
import random
from pathlib import Path
import re
import yaml
config_path = os.path.join(os.path.dirname(__file__), 'spider.yaml')

path_matcher = re.compile(r'\$\{([^}^{]+)\}')


def path_constructor(loader, node):
    """ Extract the matched value, expand env variable, and replace the match """
    value = node.value
    match = path_matcher.match(value)
    env_key_value_pair = match.group()[2:-1].split(',')
    if len(env_key_value_pair) == 2:
        env_val = os.environ.get(env_key_value_pair[0].strip(), env_key_value_pair[1].strip())
    else:
        env_val = os.environ.get(env_key_value_pair[0].strip())
    if env_val.isdigit():
        return int(env_val)
    return env_val


yaml.add_implicit_resolver('!path', path_matcher)
yaml.add_constructor('!path', path_constructor)

with open(config_path, encoding='utf-8') as f:
    cont = f.read()

cf = yaml.load(cont)


def get_db_args():
    return cf.get('db')


def get_redis_args():
    return cf.get('redis')


def get_timeout():
    return cf.get('time_out')


def get_crawl_interal():
    interal = random.randint(cf.get('min_crawl_interal'), cf.get('max_crawl_interal'))
    return interal


def get_excp_interal():
    return cf.get('excp_interal')


def get_max_repost_page():
    return cf.get('max_repost_page')


def get_max_search_page():
    return cf.get('max_search_page')


def get_max_home_page():
    return cf.get('max_home_page')


def get_max_comment_page():
    return cf.get('max_comment_page')


def get_max_dialogue_page():
    return cf.get('max_dialogue_page')


def get_max_retries():
    return cf.get('max_retries')


def get_broker_and_backend():
    redis_info = cf.get('redis')
    password = redis_info.get('password')
    sentinel_args = redis_info.get('sentinel', '')
    db = redis_info.get('broker', 5)
    if sentinel_args:
        broker_url = ";".join('sentinel://:{}@{}:{}/{}'.format(password, sentinel['host'], sentinel['port'], db) for
                              sentinel in sentinel_args)
        return broker_url
    else:
        host = redis_info.get('host')
        port = redis_info.get('port')
        backend_db = redis_info.get('backend', 6)
        broker_url = 'redis://:{}@{}:{}/{}'.format(password, host, port, db)
        backend_url = 'redis://:{}@{}:{}/{}'.format(password, host, port, backend_db)
        return broker_url, backend_url


def get_redis_master():
    return cf.get('redis').get('master', '')


def get_code_username():
    return cf.get('yundama_username')


def get_code_password():
    return cf.get('yundama_passwd')


def get_running_mode():
    return cf.get('running_mode')


def get_crawling_mode():
    return cf.get('crawling_mode')


def get_share_host_count():
    return cf.get('share_host_count')


def get_cookie_expire_time():
    return cf.get('cookie_expire_time')


def get_email_args():
    return cf.get('email')


def get_images_allow():
    return cf.get('images_allow')


def get_images_path():
    img_dir = cf.get('images_path') if cf.get('images_path') else os.path.join(str(Path.home()), 'weibospider', 'images')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    return img_dir


def get_images_type():
    return cf.get('image_type')


def get_time_after():
    return cf.get('time_after')


def get_samefollow_uid():
    return cf.get('samefollow_uid')


def get_search_args():
    return cf.get("search")
