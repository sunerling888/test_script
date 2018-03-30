#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_12_login_firstGuess_goodsDetail_addCart_loginout.py
# 登录 -> 首页猜你喜欢 -> 【随机获取猜你喜欢商品id】-> 商品详情页 -> 加入购物车（效验商品数量）->  退出登录【卖家/买家/游客】
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
class firstGuess_addCaet(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')


    # =====执行测试======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')


    
    # ================测试case===================
    '''以下是: 首页猜你喜欢 -> [随机获取猜你喜欢列表商品id] -> 商品详情页 -> 加入购物车(效验商品id是否加入) ->再次加入购物车(效验商品数量)'''
    def action_getCart(self):
        
        # 请求首页猜你喜欢
        print u'首页猜你喜欢'
        data = self.session.api('/api/mg/sale/index/getPageSecond')

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
        # re.findall是字符串类型,goodsId需要转换成int类型
        goodsId = int(re.findall(r"\d+\d*", goodsIdurl)[0])
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)

        '''
        第一次请求商品详情,添加商品id到购物车，效验goods_id、goods_number
        '''
        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        print data['code']
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
        goodsIds = {}
        activitys = cart_info['activitys']
        for item in activitys:
            if 'goods' not in item:
                continue

            # goodsIds=[goods['goods_id'] for goods in item["goods"] if 'goods_id' in goods]
            for goods in item["goods"]:
                if 'goods_id' not in goods:
                    continue
                goods_number = int(goods["goods_number"])
                goodsIds[int(goods['goods_id'])] = goods_number
                # goodsIds.append((int)(goods['goods_id']))
        # print goodsId
        # print goodsIds
        self.assertTrue(goodsId in goodsIds.keys(), u"商品不在购物车中")
        # return True


        '''
        第二次请求商品详情,添加商品id到购物车，效验goods_id、goods_number
        '''
        # 再次请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        self.assertEqual(int(data['code']), 0, data['data'])

        # 添加购物车
        print u'添加购物车'
        param = {'m': 'default', 'c': 'cart', 'a': 'add_to_cart', 'goods': urllib.quote(json.dumps({"number":1, "goods_id":goodsId}))}
        print param['goods']
        data = self.session.post('/cart.html', urllib.urlencode(param))
        print data

        # 请求购物车页
        print u'购物车页'
        response = self.session.get('/cart.html')
        # 购物车接口
        print u'购物车接口'
        response = self.session.get('/cart.html?c=cart&a=load')
        data = json.loads(response['body'])
        # print data['data']

        # 效验添加的商品数量
        cart_info = data['data']['cart_info']
        new_goodsIds= {}
        activitys = cart_info['activitys']
        for item in activitys:
            if 'goods' not in item:
                continue
            for goods in item["goods"]:
                if 'goods_id' not in goods:
                    continue
                goods_number = int(goods["goods_number"])
                new_goodsIds[int(goods["goods_id"])] = goods_number
                # goods_numbers.append((int)(goods['goods_number']))
        # print goodsId
        # print goodsIds
        print "new goods_number: %d" % new_goodsIds.get(goodsId, 0)
        print "goods_number: %d" % goodsIds.get(goodsId, 0)
        self.assertTrue((new_goodsIds.get(goodsId, 0) - goodsIds.get(goodsId, 0))==1, u"商品数量不正确")
        return True

        
    
    # =============执行case===============
    def test_01_seller_getCart(self):
        print u'卖家身份: 登录 -> 首页猜你喜欢 -> [随机获取猜你喜欢列表商品id] -> 商品详情页 -> 加入购物车(效验商品id是否加入) ->再次加入购物车(效验商品数量) -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        ret = self.action_getCart()
        self.assertTrue(ret)

    
    def test_02_user_getCart(self):
        print u'买家身份: 登录 -> 首页猜你喜欢 -> [随机获取猜你喜欢列表商品id] -> 商品详情页 -> 加入购物车(效验商品id是否加入) ->再次加入购物车(效验商品数量) -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        
        ret = self.action_getCart()
        self.assertTrue(ret)


    def test_03_no_getCart(self):
        print u'游客身份: 登录 -> 首页猜你喜欢 -> [随机获取猜你喜欢列表商品id] -> 商品详情页 -> 加入购物车(效验商品id是否加入) -> 再次加入购物车(效验商品数量) -> 退出登录'
        # self.session.api('/api/mg/auth/user/login')

        ret = self.action_getCart()
        self.assertTrue(ret)


