#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_17_login_goodsDeatil_multiple_getCheckout_loginout.py     # 多规格商品
# 步骤
    a. 搜索多规格商品
    b. 搜索结果
    c. 商品详情页
    d. 判断是普通商品、多规格商品
        e.1 普通商品:
            e.1.1 判断"childs"字段列表是否为空  *空列表==普通商品
            e.1.2 判断"childs"字段列表是否为空  *不是空列表==多规格商品     **遍历childs -> list -> 随机goodsId

            e.1.3 判断"extra -> dataList字段    *遍历dataList字段，随机goodsId   判断**goodsStocks大于0, onSale等于1**    --多规格
            e.1.4 判断"extra -> dataList字段"   判断*goodsStocks大于0, onSale等于1      --普通商品
    f. /checkout.html
'''

import requests
import unittest
import urllib,urllib2
import csv
import random
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv
from bs4 import BeautifulSoup


# 创建测试
class multiple_getCheckout(unittest.TestCase):

    # 获取test_user.csv
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    # 获取test_search_multiple_goods.csv
    searchs = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_search_multiple_goods.csv')


    # 设置初始化
    def setUp(self):
        print u'-----测试开始------'

        self.session = DavdianSession()
    
    def tearDown(self):
        print u'------测试结束------'
        self.session.api('/api/mg/auth/user/logout')

    
    # ===================测试case====================
    '''搜索商品 -> 商品详情页 -> 立即购买 -> 订单确认页'''
    def action_multiple_getCheckout(self, keywords=None):

        # 请求搜索接口
        print u'首页搜索'
        data = self.session.api('/api/mg/sale/index/getSearch')
        self.assertEqual(int(data['code']), 0, data['data'])

    
        # 搜索结果
        print u'搜索结果'
        param = {'keywords':keywords['keywords'], 'h5Platform': keywords['h5Platform'], 'pageIndex': keywords['pageIndex'], 'pageSize': keywords['pageSize'], 'sort': keywords['sort']}
        data = self.session.api('/api/mg/sale/search/getGoods', param)
        self.assertEqual(int(data['code']), 0, data['data'])

        # 搜索结果取出goodsId -> 随机goodsId(商品详情)
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
        # sales = 0
        # status = 0
        while True:     # 循环直到取到sales里的goodsStocks大于0，status里的onSale不等于1
            randIndex = random.randint(0, length - 1)
            content = contents[randIndex]

            goodsIdurl = contents[randIndex]
            goodsId = int(re.findall(r"\d+\d*", goodsIdurl)[0])
            print "DEBUG\t[%s][%s]" %(u'goodsId', goodsId)


            # 请求商品详情页接口
            print u'商品详情页'
            print "DEBUG\t[%s][%s]" %(u'goodsId', goodsId)
            param = {'goodsId':goodsId}
            data = self.session.api('/api/mg/good/info/detail', param)
            # print json.dumps(data)

            # 判断多规格商品
            basis = data['data']['basis']
            goodsName = basis['goodsName']
            print goodsName
            if not basis.has_key('childs'):
                return (False, '')
            if len(basis['childs']) < 0:
                return (False, '')
            # 取出childs -> list -> title
            childs = basis['childs']
            if not childs.has_key('list') or len(childs['list']) == 0:
                return (False, '')
            list = childs['list'][0]
            title = childs['list'][0]['title']
            print title
            extra = data['data']['extra']
            if not extra.has_key('dataList') or len(extra['dataList']) == 0:
                return (False, '')
            dataList = extra['dataList'][0]
            sales = dataList['sales']['goodsStocks']
            status = dataList['status']['onSale']
            print sales,status
            if int(sales) > 0:
                print "***********************"
                print sales
                print "***********************"
                break
        # 多规格商品拼接: goodsName + title
        goodsNames = goodsName + '_' + title
        print goodsNames

        # 请求订单确认页
        if sales == 0 and status != 1:
            return (False, '')
        param = {'goods[0][id]': str(goodsId), 'goods[0][number]': '1'}
        response = self.session.get('/checkout.html?rp=goods_detail&rl=checkout' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)

        # 判断确认订单页商品名称
        # 取出response['body']里的商品名称
        result = False
        soup = BeautifulSoup(response['body'], 'html.parser')
        content = soup.find_all("div", class_='good_title')
        print content
        # 获取good_title里的值
        if len(content) > 0:
            content = content[0].get_text().strip()
            print "content************"
            print content
            print "content************"
            if goodsNames == content:
                result = True
            self.assertTrue(result, u'商品不存在!')

        return (result, response['body'])

    
    # =============执行case==============

    def test_01_seller_multiple_getCheckout(self):
        print u'卖家身份:'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        query = self.searchs.random()
        ret, body = self.action_multiple_getCheckout(query)
        self.assertTrue(ret)

    
    def test_02_user_multiple_getCheckout(self):
        print u'买家身份:'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        query = self.searchs.random()
        ret, body = self.action_multiple_getCheckout(query)
        self.assertTrue(ret)

    
    def test_03_no_multiple_getCheckout(self):
        print u'游客身份:'

        query = self.searchs.random()
        ret, body = self.action_multiple_getCheckout(query)
        # 取出sess_key
        sess_key = self.session.session
        print sess_key

        result = False
        if 'js/login.js' in body:
            result = True
        self.assertTrue(result)