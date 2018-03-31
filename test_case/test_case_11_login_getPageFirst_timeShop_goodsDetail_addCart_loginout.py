#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''test_case_11_login_getPageFirst_timeShop_goodsDetail_getCart_loginout.py
# 登录 -> 首页(第一屏) -> 【随机获取限时购商品id】 -> 商品详情页 -> 加入购物车（效验添加的商品id） -> 退出登录【卖家/买家/游客】
'''

import requests
import unittest
import urllib,urllib2
import csv
import json
import random
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv


# 创建测试
class timeShop_addCart(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    # '''获取test_cart.csv文件'''
    # carts = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_cart.csv')


    # =====执行测试======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')


    # ==============测试case==================
    '''以下是:登录 -> 首页(第一屏) -> 【随机获取第一屏/限时购列表商品id】 -> 商品详情页 -> 加入购物车 -> 退出登录'''
    def action_getCart(self):

        # 请求首页第一屏
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')

        feedList = data['data']['feedList']
        goodsIds = []
        for item in feedList:
            if 'body' not in item or 'dataList' not in item['body']:
                continue
            if len(item['body']['dataList']) < 1 or 'goodsId' not in item['body']['dataList'][0]:
                continue
            goodsIds.append((int)(item['body']['dataList'][0]['goodsId']))

        length = len(goodsIds)
        randIndex = random.randint(0, length - 1)

        goodsId = goodsIds[randIndex]
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        # self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)


        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        # return True

        
        # 添加购物车
        print u'添加购物车'
        # 添加购物车的接口，需要goods: {"number":1,"goods_id":"550358"},用urllib.quote的方式
        param = {'m': 'default', 'c': 'cart', 'a': 'add_to_cart', 'goods': urllib.quote(json.dumps({"number":1, "goods_id":goodsId}))}
        print param['goods']
        # 购物车这里直接用post请求，**需要urlencode**
        data = self.session.post('/cart.html', urllib.urlencode(param))
        print data
        # self.assertEqual(int(data['code']), 0, data['data'])


        # 请求购物车页面
        print u'购物车页面'
        response = self.session.get('/cart.html')
        # print response
        # return "购物车" in response['body']
        

        # 请求购物车接口
        print u'购物车接口'
        response = self.session.get('/cart.html?c=cart&a=load')
        # print response

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
    def test_01_seller_getCart(self):
        print u'卖家身份: 登录 -> 首页(第一屏) -> 【随机获取限时购商品id】 -> 商品详情页 -> 加入购物车（效验添加的商品id）-> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        # cart = self.carts.random()
        ret = self.action_getCart()
        self.assertTrue(ret)

    
    def test_02_user_addCart(self):
        print u'买家身份: 登录 -> 首页(第一屏) -> 【随机获取限时购商品id】 -> 商品详情页 -> 加入购物车（效验添加的商品id）-> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        ret = self.action_getCart()
        self.assertTrue(ret)
    

    def test_03_no_addCart(self):
        print u'游客身份: 登录 -> 首页(第一屏) -> 【随机获取限时购商品id】 -> 商品详情页 -> 加入购物车（效验添加的商品id）-> 退出登录'

        # self.session.api('/api/mg/auth/user/login')
        # self.assertEqual(int(data['code']), 0, data['data'])
        ret = self.action_getCart()
        # print ret
        self.assertTrue(ret)    
    