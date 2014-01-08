#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import urllib, urllib2, urlparse
import time
import anyjson
import pymongo

ROOT_URL='https://kyfw.12306.cn/otn/'

mong_col = pymongo.MongoClient('192.168.1.100', 27017)['cn12306']['web_resp_time']

def get_web_resp(fullurl):
    # fullurl = urlparse.urljoin(ROOT_URL, url_path)
    t1 = time.time()
    resp = urllib2.urlopen(fullurl)
    t2 = time.time()
    resp_time_msecs = int((t2-t1) * 1000)
    info = resp.info()
    headers = {}
    for h in info.headers:
        name = h.split(':')[0]
        headers[name] = info.getheader(name)
    headers['url'] = resp.geturl()
    headers['resp_time_msecs'] = resp_time_msecs
    headers['request_time'] = t1
    mong_col.insert(headers)
    return headers

if __name__ == '__main__':
    url_list = []
    url_list.append('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2014-01-24&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=WCN&purpose_codes=ADULT')
    url_list.append('https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=6c000G11080B&from_station_no=01&to_station_no=08&seat_types=OMP&train_date=2014-01-24')
    url_list.append('https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=6c000G111803&from_station_telecode=IZQ&to_station_telecode=WHN&depart_date=2014-01-24')
    url_list.append('https://kyfw.12306.cn/otn/login/checkUser')
    url_list.append('https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew.do?module=login&rand=sjrand&0.23189895111136138')

    for i in url_list:
        get_web_resp(i)

