# -*- coding: utf-8 -*-

import requests
import time
import os
import csv
import sys
import json
from bs4 import BeautifulSoup
import importlib
importlib.reload(sys)

url = 'https://m.weibo.cn/comments/hotflow?id=4477585038109216&mid=4477585038109216&max_id='
headers = {
    'cookie': 'ALF=1585370472; _T_WM=29782310930; SCF=An5xEz9A55-FA7deRTpOHiSWp20FZdDhvd9HwCjUgictHuauMl9SxjzF9NE4q09x6NU8w_JuXomkC8JM1VHAZgw.; SUB=_2A25zUz2gDeRhGeFN6FQT8izIzDWIHXVQvEPorDV6PUJbktANLWPxkW1NQCE2BjG1vTrhKEjLYvX3Yu1qLi84_4TT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5QVRlHLCOnVPQaYb_ZkJnp5JpX5K-hUgL.FoM0e0qEeozXS0.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNe0eceozEShM4; SUHB=0jBIAwbzeCKoI6; WEIBOCN_FROM=1110106030; MLOGIN=1; XSRF-TOKEN=7b3cf3; M_WEIBOCN_PARAMS=oid%3D4477585038109216%26luicode%3D20000061%26lfid%3D4477585038109216%26uicode%3D20000061%26fid%3D4477585038109216',
    'referer': 'https://m.weibo.cn/detail/4477585038109216',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'

}

def get_page(max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)


def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
        item_max_id['max_id_type'] = items['max_id_type']
        return item_max_id

def write_csv(jsondata):
    datas = jsondata.get('data').get('data')
    for data in datas:
        created_at = data.get("created_at")
        like_count = data.get("like_count")
        source = data.get("source")
        floor_number = data.get("floor_number")
        username = data.get("user").get("screen_name")
        comment = data.get("text")
        comment = BeautifulSoup(comment, 'lxml').get_text()
        writer.writerow([username, created_at, like_count, floor_number, source, json.dumps(comment, ensure_ascii=False)])

path = os.getcwd() + "/weiboComments.csv"
csvfile = open(path, 'w', encoding = 'utf-8')
writer = csv.writer(csvfile)
writer.writerow(['Usename', 'Time', 'Like_count', 'Floor_number', 'Sourse', 'Comments'])


maxpage = 50
m_id = 0
id_type = 0
for page in range(0, maxpage):
    print(page)
    jsondata = get_page(m_id, id_type)
    write_csv(jsondata)
    results = parse_page(jsondata)
    time.sleep(1)
    m_id = results['max_id']
    id_type = results['max_id_type']