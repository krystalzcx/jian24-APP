import datetime
import os
import time
import requests
from httprunner.api import HttpRunner

COOKIES_PATH = r'data/cookies'
ID_of_promotion_PATH=r'data/ID'
#ID_of_promotion=''

def sleep(n_secs):
    time.sleep(n_secs)

#产生一个时间戳后缀
def name_suffix_of_time_stamp():
    name_suffix=str(int(time.time()))
    return name_suffix

def get_date():
    today=str(datetime.date.today())
    print(today)
    return today

def get_promtion_start_time():
    today = str(datetime.date.today())
    start=today+' 00:00:00'
    return start
def get_promtion_end_time():
    today = str(datetime.date.today())
    end=today+' 23:59:59'
    return end

#禁用之前的冲突的单品促销
def disable_promtion():
    #判断存放单品促销ID文件是否为空，即为ID是否存在
    if os.path.getsize(ID_of_promotion_PATH)!=0:
        runner = HttpRunner()
        runner.run(r'api/disable_promotion.yml')


#方式1：获取新建的状态未启用的单品促销ID_of_promotion_of_promotion
def get_first_promotion_id(response):
    id=str(response.json['info']['data'][0]['id'])
    status=response.json['info']['data'][0]['status_name']
    if status != '禁用':
        with open(ID_of_promotion_PATH, 'w') as f:
            f.write(id)
    print(id)
    return id

#为api/disable_promotion.yml提供id
def get_ID_of_promotion():
    #实际应该考虑若第一个不是禁用状态的促销该怎么办
    if os.path.getsize(ID_of_promotion_PATH)!=0:
        with open(ID_of_promotion_PATH, 'r') as f:
            id: str = f.read()
    return id

# #方式2：获取新建的状态未启用的单品促销ID_of_promotion
# def get_promotion_ID_of_promotion_2():
#     runner=HttpRunner()
#     response=runner.run(r'api/search_promotion.yml')
#     print('方式2')
#     print(response)
#     # id = response['info']['data'][0]['ID_of_promotion']
#     # status = response['info']['data'][0]['status_name']
#     # if status != '禁用':
#     #     ID_of_promotion = id
#     # else:
#     #     ID_of_promotion = ''
#     return ID_of_promotion




# 判断是不是superuser账号
def get_is_superuser(username):
    if username == 'admin':
        return True
    else:
        return False

#商品信息导入接口需要把导入的文件参数转化为二进制
#问题:转为二进制的形式与实际请求的时候不一致
def importFile_changeTo_binary():
    path=r'data/product_info_import_template'
    with open(path, 'r') as f:
        file_info: str = f.read()
    binary_file = bytes(file_info, encoding="utf8")
    print(binary_file)
    return binary_file

'''
断言某种搜索条件下第一页的记录数量:
某种搜索条件下的实际查询结果总数量记为A
接口展示的记录只是当前页的数据，记录数记为B
若A>20，那么B=20;若A<20，那么B=A
'''

def numberOfRecords_paging(total_count):
    first_page_count = 0
    if total_count > 20:
        first_page_count = 20
    else:
        first_page_count = total_count
    print("第一页的记录数量是："+str(total_count))
    return first_page_count


'''
调用teardown_saveCookies()函数，读取cookies
若还从未读取过cookies(即为从未执行过testcases/login.yml)或者已经过期，
那么需要执行testcases/login.yml,从而获取cookies
'''


def generate_cookies():
    if (not os.path.exists(COOKIES_PATH)) or (
            3600 < int(time.time()) - int(os.path.getmtime(COOKIES_PATH))) or (os.path.getsize(COOKIES_PATH)==0):
        # cookies 文件不存在 或 最后修改时间超过 3600 秒 (1小时) 或 cookie文件内容为空 则重新登录刷新 cookies
        runner = HttpRunner()
        runner.run(r'api/login.yml')
    with open(COOKIES_PATH, 'r') as f:
        cookies: str = f.read()
    print("读取文件内cookie"+cookies)
    return cookies


'''
编写hook函数(yml文件的teardown_hooks会调用)：
从接口的reponse里获取cookies
转为字符串，存入文件路径COOKIES_PATH
'''


def teardown_saveCookies(response: requests.Response):
    """保存 cookies 到文件给其他 api 调用"""
    cookies: dict = response.cookies
    # cookies =dict(response.cookies)
    foo: list = []
    # 遍历 cookies 拆分 dict 并拼接为特定格式的 str
    # 如: server=xxxxx; sID_of_promotion=xxxxxx; track=xxxxx;
    for k, v in cookies.items():
        foo.append(k + '=' + v + '; ')
    # join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
    bar: str = "".join(foo)
    with open(COOKIES_PATH, 'w') as f:
        f.write(bar)
    print("重新写入cookie"+bar)

def hook_print(a):
    print(a)