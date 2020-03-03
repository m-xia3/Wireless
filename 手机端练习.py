# -*- coding: utf-8 -*-


import requests
import time
import os
import csv
import sys
import json
# from bs4 import BeautifulSoup
import importlib
importlib.reload(sys)
from pyquery import PyQuery

url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'cookie': 'ALF=1585370472; _T_WM=29782310930; WEIBOCN_FROM=1110006030; SCF=An5xEz9A55-FA7deRTpOHiSWp20FZdDhvd9HwCjUgictHuauMl9SxjzF9NE4q09x6NU8w_JuXomkC8JM1VHAZgw.; SUB=_2A25zUz2gDeRhGeFN6FQT8izIzDWIHXVQvEPorDV6PUJbktANLWPxkW1NQCE2BjG1vTrhKEjLYvX3Yu1qLi84_4TT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5QVRlHLCOnVPQaYb_ZkJnp5JpX5K-hUgL.FoM0e0qEeozXS0.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNe0eceozEShM4; SUHB=0jBIAwbzeCKoI6; SSOLoginState=1582779888; MLOGIN=1; XSRF-TOKEN=f7b78f; M_WEIBOCN_PARAMS=luicode%3D20000174%26lfid%3D1076032936828821%26uicode%3D20000174',
    'referer': 'https://m.weibo.cn/profile/2936828821',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

def get_page(page):
    params = {
        'containerid': '2304132936828821',
        'page_type' : '03',
        'page': 'page'
    }
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)

def write_csv(jsondata):
    datas = jsondata.get('data').get('cards')
    for data in datas:
        created_at = data.get("mblog").get("created_at")
        text = PyQuery(data.get("mblog").get("text")).text()
        source = data.get("mblog").get("source")
        screen_name = data.get("user").get("screen_name")
        write.writerow([screen_name, created_at, source, text])


path = os.getcwd() + "/Zhujianizi.csv"
csvfile = open(path, 'w',encoding = 'utf-8')
writer = csv.writer(csvfile)
writer.writerow(['screen_name', 'created_at', 'source', 'text'])


def main():
    for page in range(1,500):
        r.json = get_page(page)
        results = write_csv(r.json)

#maxpage = 101
#for page in range(0, maxpage):
#    print(page)
#    jsondata = get_page(page)
#    write_csv(jsondata)





