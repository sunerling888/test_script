#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_21_login_search_buyGoods_orderpay_loginout.py
# 登录 -> 搜索商品 -> 商品详情页 -> 购买 -> 订单确认 -> 支付完成
'''

import requests
import unittest
import urllib,urllib2
import csv
import json
import re
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv
from bs4 import BeautifulSoup


# 创建测试
class search_buyGoods_pay(unittest.TestCase):

    '''获取test_user.csv'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    '''获取test_search_goods_buy.csv'''
    searchs = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_search_goods_buy.csv')


    
    # ======执行测试=======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')


    # ============测试case================
    '''以下是:搜索商品 -> 商品详情页 -> 立即购买 -> 订单确认页 -> 支付vdone -> 完成支付'''
    def action_search_buyGoods_pay(self, keywords=None):

        # 请求首页搜索
        print u'首页搜索'
        data = self.session.api('/api/mg/sale/index/getSearch')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        
        # 请求搜索结果
        print u'搜索结果'
        param = {'keywords':keywords['keywords'], 'h5Platform': keywords['h5Platform'], 'pageIndex': keywords['pageIndex'], 'pageSize': keywords['pageSize'], 'sort': keywords['sort']}
        data = self.session.api('/api/mg/sale/search/getGoods', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        # 取出goodsId,随机goodsId
        feedList = data['data']['feedList']
        contents = []
        for item in feedList:
            if not item.has_key('body') or not item['body'].has_key('dataList'):
                continue
            if len(item['body']['dataList']) < 0:
                continue

            dataList = item['body']['dataList']
            for data in dataList:
                if not data.has_key('command'):
                    continue
                if not data['command'].has_key('content'):
                    continue
                if re.match(r'^/\d+.html', data['command']['content']):
                    contents.append(data['command']['content'])

        length = len(contents)
        randIndex = random.randint(0, length - 1)
        content = contents[randIndex]

        goodsIdurl = contents[randIndex]
        goodsId = int(re.findall(r"\d+\d*", goodsIdurl)[0])
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)


        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        # print json.dumps(data)


