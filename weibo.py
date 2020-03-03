# -*- coding: utf-8 -*-

import requests
from urllib.parse import urlencode
from pyquery import PyQuery
import pprint
import os
import csv
import sys
base_url = 'https://m.weibo.cn/api/container/getIndex?'

#代码块 请求的方法
#根据页数获取数据
def get_page(page):
    prames = {
        "containerid":"2304132936828821",
        "page_type":"03",
        "page": page
    }
    response = requests.get(base_url + urlencode(prames))
    return response.json()

#解析数据
def prase_data(res_json):
    if res_json.get("data"):
        for node in res_json["data"]["cards"]:
            prase_data(node)
            item = dict()
            item["text"] = PyQuery(node["mblog"]["text"]).text()
            item["id"] = node["mblog"]["id"]
            item["screen_name"] = node["mblog"]["user"]["screen_name"]
            item["comments_count"] = node["mblog"]["comments_count"]
            writer.writerow(item)
            print(item)


path = os.getcwd() + "/Zhujianizi.csv"
csvfile = open(path, 'w',encoding = 'utf-8')
writer = csv.writer(csvfile)
writer.writerow(['screen_name', 'id', 'text', 'comments_count'])

def main():
    for page in range(1,50):
        res_json = get_page(page)
        prase_data(res_json)

if __name__ == '__main__':
    main()

#调用代码块 get_page()