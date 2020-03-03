# -*- coding: utf-8 -*-

import wx
import sys
import urllib
import urllib.request
import re
import json
import hasnlib
import os
import time
from datetime import datetime
from datetime import timedelta
import random
from lxml import etree
import logging
import xlwt
import xlrd
from xlutils.copy import copy


class CollectData():
    def __init__(self, keyword, startTime, interval='50', flag=True, begin_url_per = "https://s.weibo.com/weibo/"):
        self.begin_url_per = begin_url_per
        self.setKeyword(keyword)
        self.setStartTimescope(startTime)
        self.setRegion(region)
        self.setInterval(interval)
        self.setFlag(flag)
        self.logger = logging.getLogger('main.CollectData')

    def setKeyword(self, keyword):
        self.keyword = keyword.decode('GBK','ignore').encode("utf-8")
        print ('twice encode:'), self.getKeyWord()

    def getKeyWord(self):
        once = urllib.urlencode({"kw": self.keyword})[3:]
        return urllib.urlencode({"kw": once})[3:]

    def setStartTimescope(self, startTime):
        if not (startTime == '-'):
            self.timescope = startTime + ":" + startTime
        else:
            self.timescope = '-'

    def setInterval(self, interval):
        self.interval = int(interval)

    def setFlag(self, flag):
        self.flag = flag

    def getURL(self):
        return self.begin_url_per + self.getKeyWord() + "&typeall=1&suball=1×cope=custom:" + self.timescope + "&page="

    def download(self, url, maxTryNum=4):
        hasMore = True
        isCaught = False
        name_filter = set([])
        i = 1
        while hasMore and i < 51 and (not isCaught):
            source_url = url + str(i)
            data = ''
            goon = True
            for tryNum in range(maxTryNum):
                try:
                    html = urllib2.urlopen(source_url, timeout=12)
                    data = html.read()
                    break
                except:
                    if tryNum < (maxTryNum - 1):
                        time.sleep(10)
                    else:
                        print ('Internet Connect Error!')
                        self.logger.error('Internet Connect Error!')
                        self.logger.info('url: ' + source_url)
                        self.logger.info('fileNum: ' + str(fileNum))
                        self.logger.info('page: ' + str(i))
                        self.flag = False
                        goon = False
                        break
            if goon:
                lines = data.splitlines()
                isCaught = True
                for line in lines:
                    if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
                        isCaught = False
                        n = line.find('html":"')
                        if n > 0:
                            j = line[n + 7: -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\", "")
                            if (j.find('<div class="search_noresult">') > 0):
                                hasMore = False
                            else:
                                page = etree.HTML(j.decode('utf-8'))
                                ps = page.xpath("//p[@node-type='feed_list_content']")
                                addrs = page.xpath("//a[@class='W_texta W_fb']")
                                addri = 0
                                for p in ps:
                                    name = p.attrib.get('nick-name')
                                    txt = p.xpath('string(.)')
                                    addr = addrs[addri].attrib.get('href')
                                    addri += 1
                                    if (name != 'None' and str(txt) != 'None' and name not in name_filter):
                                        name_filter.add(name)
                                        oldWb = xlrd.open_workbook('weiboData.xls', formatting_info=True)
                                        oldWs = oldWb.sheet_by_index(0)
                                        rows = int(oldWs.cell(0, 0).value)
                                        newWb = copy(oldWb)
                                        newWs = newWb.get_sheet(0)
                                        newWs.write(rows, 0, str(rows))
                                        newWs.write(rows, 1, name)
                                        newWs.write(rows, 2, self.timescope)
                                        newWs.write(rows, 3, addr)
                                        newWs.write(rows, 4, txt)
                                        newWs.write(0, 0, str(rows + 1))
                                        newWb.save('weiboData.xls')
                                        print ('save with same name ok')
                        berak
                lines = None
                if isCaught:
                    print ('Be Caught!')
                    self.logger.error('Be Caught Error!')
                    self.logger.info('filePath: ' + savedir)
                    self.logger.info('url: ' + source_url)
                    self.logger.info('fileNum: ' + str(fileNum))
                    self.logger.info('page:' + str(i))
                    data = None
                    self.flag = False
                    break
                if not hasMore:
                    print ('No More Results!')
                    if i == 1:
                        time.sleep(random.randint(3, 8))
                    else:
                        time.sleep(10)
                    data = None
                    break
                i += 1
                if i % 2 == 0:
                    sleeptime = sleeptime_two
                else:
                    sleeptime = sleeptime_one
                print ('sleeping ' + str(sleeptime) + ' seconds...')
                time.sleep(sleeptime)
            else:
                break

    def getTimescope(self, perTimescope):
        if not (perTimescope == '-'):
            times_list = perTimescope.split(':')
            start_date = datetime(int(times_list[-1][0:4]), int(times_list[-1][5:7]), int(times_list[-1][8:10]))
            start_new_date = start_date + timedelta(days=1)
            start_str = start_new_date.strftime("%Y-%m-%d")
            return start_str + ":" + start_str
        else:
            return '-'

    def main():
        logger = logging.getLogger('main')
        logFile = './collect.log'
        logger.setLevel(logging.DEBUG)
        filehandler = logging.FileHandler(logFile)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

        while True:
            keyword = raw_input('Enter the keyword(type \'quit\' to exit ):')
            if keyword == 'quit':
                sys.exit()
            startTime = raw_input('Enter the start time(Format:YYYY-mm-dd):')
            region = raw_input('Enter the region([BJ]11:1000,[SH]31:1000,[GZ]44:1,[CD]51:1):')
            interval = raw_input('Enter the time interval( >30 and deafult:50):')
            cd = CollectData(keyword, startTime, interval)
            while cd.flag:
                print ('cd.timescope')
                logger.info(cd.timescope)
                url = cd.getURL()
                cd.download(url)
                cd.timescope = cd.getTimescope(cd.timescope)
            else:
                cd = None
                print ('-----------------------------------------------------')
                print ('-----------------------------------------------------')
        else:
            logger.removeHandler(filehandler)
            logger = None
if __name__ == '__main__':
    main()




















