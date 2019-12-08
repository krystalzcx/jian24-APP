import os
import time
import requests
from httprunner.api import HttpRunner

COOKIES_PATH = r'data/cookies'


def sleep(n_secs):
    time.sleep(n_secs)


# 判断是不是superuser账号
def is_superuser():
    env = os.environ["USERNAME"]
    if env == 'admin':
        return True
    else:
        return False


# 获取加盟商的名字
def franchisee_name():
    var = 'superuser'
    if is_superuser():
        var = 'superuser'
    else:
        var = 'not_sure'
    return var


'''
调用teardown_saveCookies()函数，读取cookies
若还从未读取过cookies(即为从未执行过testcases/login.yml)或者已经过期，
那么需要执行testcases/login.yml,从而获取cookies
'''


def generate_cookies():
    if (not os.path.exists(COOKIES_PATH)) or (
            3600 < int(time.time()) - int(os.path.getctime(COOKIES_PATH))):
        # cookies 文件不存在 或 最后修改时间超过 3600 秒 (1小时) 则重新登录刷新 cookies
        runner = HttpRunner()
        runner.run(r'api/login.yml')
    with open(COOKIES_PATH, 'r') as f:
        cookies: str = f.read()
    return cookies


'''
编写hook函数(yml文件的teardown_hooks会调用)：
从接口的reponse里获取cookies
转为字符串，存入文件路径COOKIES_PATH
'''


def teardown_saveCookies(response: requests.Response):
    """保存 cookies 到文件给其他 api 调用"""
    cookies: dict = response.cookies
    #cookies =dict(response.cookies)

    foo: list = []
    # 遍历 cookies 拆分 dict 并拼接为特定格式的 str
    # 如: server=xxxxx; sid=xxxxxx; track=xxxxx;
    for k, v in cookies.items():
        foo.append(k + '=' + v + '; ')
    bar: str = "".join(foo)
    with open(COOKIES_PATH, 'w') as f:
        f.write(bar)
