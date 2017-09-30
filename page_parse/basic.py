from bs4 import BeautifulSoup

from decorators import parse_decorator


@parse_decorator(False)
def is_404(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 前一种情况是处理直接用js实现重定向的页面
    try:
        if "http://weibo.com/sorry?pagenotfound" in html:
            return True
        elif soup.title.text == '404错误':
            return True
        elif html == '':
            return True
        # 处理转发微博的情况
        elif '抱歉，此微博已被作者删除' in html:
            return True
        else:
            return False
    except AttributeError:
        return False


@parse_decorator(False)
def is_403(html):
    if "['uid']" not in html and "['nick']" not in html:
        return True

    # verify code for search page
    # todo  solve the problem of verify_code when searching
    if 'yzm_img' in html and 'yzm_input' in html:
        return True

    soup = BeautifulSoup(html, 'html.parser')
    if soup.title:
        if '访问受限' in soup.title.text or '解冻' in soup.title.text:
            return True
        else:
            return False
    else:
        return False


def is_complete(html):
    return True if 'uid' in html else False


