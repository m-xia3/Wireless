# -*- coding: utf-8 -*-

import requests
import re
import time
def get_one_page(url):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'Host': 'm.weibo.cn',
        'Accept': 'application/json, text/plain, */*',
        'Accept-language': 'en-US,en;q=0.9',
        'Accept-encoding': 'gzip, deflate, br',
        'Cookie': '_T_WM=29782310930; ALF=1585628763; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5QVRlHLCOnVPQaYb_ZkJnp5JpX5K-hUgL.FoM0e0qEeozXS0.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNe0eceozEShM4; SCF=An5xEz9A55-FA7deRTpOHiSWp20FZdDhvd9HwCjUgictfyEq6TExHAbK3knToops23KdLJP66gg7lRmVpnWkuE4.; SUB=_2A25zWAVHDeRhGeFN6FQT8izIzDWIHXVQoqsPrDV6PUJbktANLRShkW1NQCE2BgntdNdURcg_H0nA2pmkiQsfniSx; SUHB=0LcSayk-jcY4Me; SSOLoginState=1583117591; MLOGIN=1; XSRF-TOKEN=2661c3; WEIBOCN_FROM=1110106030; M_WEIBOCN_PARAMS=oid%3D4185205713444106%26lfid%3D1076032936828821%26luicode%3D20000174%26uicode%3D20000174',
        'DNT': '1',
        'Connection': 'keep-alive'

     }
    response = requests.get(url,headers = headers,verify = False)
    if response.status_code == 200:
        return response.text
    return None
def parse_one_page(html):
    pattern = re.compile('<span class="ctt">.*?</span>', re.S)
    items = re.findall(pattern, html)
    result = str(items)
    with open('test.txt', 'a', encoding='utf-8') as fp:
        fp.write(result)

for i in range(20):
    url = "https://m.weibo.cn/api/container/getIndex?containerid=2304132936828821&page_type=03&page="+str(i)
    html = get_one_page(url)
    print(html)
    print('正在爬取第 %d 页' % (i + 1))
    parse_one_page(html)
    time.sleep(3)


