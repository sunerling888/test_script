#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_13_login_getSearch_goodsDetail_addCart_loginout.py
# 登录 -> 搜索商品 -> 商品详情页 -> 加入购物车 -> [效验商品id] -> 退出登录
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



# 创建测试
class serach_addCart(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    '''获取test_search.csv文件'''
    searchs = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_search_goods.csv')


    # =======执行测试========
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')


    
    # ===================测试case====================
    '''以下: 搜索商品 -> 商品详情页 -> 加入购物车【效验商品id】 '''
    def action_search_addCart(self, keywords=None):

        # 请求首页搜索接口
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
                # print (data['command']['content'])
                if not data.has_key('command'):
                    continue
                if not data['command'].has_key('content'):
                    continue
                if re.match(r'^/\d+.html', data['command']['content']):
                    contents.append(data['command']['content'])
        # print contents

        length = len(contents)

        randIndex = random.randint(0, length - 1)
        content = contents[randIndex]

        goodsIdurl = contents[randIndex]
        goodsId = int(re.findall(r"\d+\d*", goodsIdurl)[0])
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)


        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId':goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        # print json.dumps(data)


        # 添加购物车
        print u'添加购物车'
        # 添加购物车的接口，需要goods: {"number":1,"goods_id":"550358"},用urllib.quote的方式
        param = {'m': 'default', 'c': 'cart', 'a': 'add_to_cart', 'goods': urllib.quote(json.dumps({"number":1, "goods_id":goodsId}))}
        print param['goods']
        data = self.session.post('/cart.html', urllib.urlencode(param))
        print data

        # 请求购物车页
        print u'购物车页'
        response = self.session.get('/cart.html')
        # 请求购物车接口
        print u'购物车接口'
        response = self.session.get('/cart.html?c=cart&a=load')
        
        data = json.loads(response['body'])

        
        # 以下:效验随机加入的商品id是不是在购物车中
        cart_info = data['data']['cart_info']
        goodsIds = []
        activitys = cart_info['activitys']
        for item in activitys:
            if 'goods' not in item:
                continue

            # goodsIds=[goods['goods_id'] for goods in item["goods"] if 'goods_id' in goods]
            for goods in item["goods"]:
                if 'goods_id' not in goods:
                    continue
                goodsIds.append((int)(goods['goods_id']))
        # print goodsId
        # print goodsIds
        self.assertTrue(goodsId in goodsIds, u"商品不在购物车中")
        return True


    # =============执行case===============
    def test_01_seller_search_addCart(self):
        print u'卖家身份:登录 -> 搜索商品 -> 商品详情页 -> 加入购物车 -> [效验商品id] -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        query = self.searchs.random()
        ret = self.action_search_addCart(query)
        self.assertTrue(ret)


    def test_02_user_search_addCart(self):
        print u'买家身份:登录 -> 搜索商品 -> 商品详情页 -> 加入购物车 -> [效验商品id] -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        query = self.searchs.random()
        ret = self.action_search_addCart(query)
        self.assertTrue(ret)

    
    def test_03_no_search_addCart(self):
        print u'游客身份:登录 -> 搜索商品 -> 商品详情页 -> 加入购物车 -> [效验商品id] -> 退出登录'

        query = self.searchs.random()
        ret = self.action_search_addCart(query)
        self.assertTrue(ret)