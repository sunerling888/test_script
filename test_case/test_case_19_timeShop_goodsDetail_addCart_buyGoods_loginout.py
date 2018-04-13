#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_19_timeShop_goodsDetail_addCart_buyGoods_loginput.py
# 登录 -> 首页限时购 -> 随机商品 -> 商品详情页 -> 加入购物车 -> 订单确认 -> 去支付 -> 生成订单 -> 退出登录
'''

import requests
import unittest
import urllib,urllib2
import csv
import json
import random
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv


# 创建测试
class timeShop_getCart_buy(unittest.TestCase):
    
    '''获取user_csv'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')


    # =====执行测试=====
    def setUp(self):
        print u'----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')

    
    # ============测试case================
    '''以下是: 登录 -> 首页限时购 -> [随机限时购商品] -> 商品详情页 -> 加入购物车 -> 订单确认 -> 去支付生成订单'''
    def action_timeShop_getCart_buy(self):

        # 请求首页限时购
        print u'首页限时购'
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


        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId':goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        # print data
        self.assertEqual(int(data['code']), 0, data['data'])
        # 判断普通商品
        basis = data['data']['basis']
        goodsName = basis['goodsName']
        print goodsName
        if not basis.has_key('childs'):
            return (False, '')
        if len(basis['childs']) > 0:
            return (False, '')
        extra = data['data']['extra']
        if not extra.has_key('dataList') or len(extra['dataList']) == 0:
            return (False, '')
        dataList = extra['dataList'][0]
        sales = dataList['sales']['goodsStocks']
        status = dataList['status']['onSale']
        print sales,status

        # 加入购物车
        print u'加入购物车'
        param = {'goods': urllib.quote(json.dumps({"number":1, "goods_id":goodsId}))}
        print param['goods']
        data = self.session.post('/index.php?c=cart&a=add_to_cart&m=default', urllib.urlencode(param))


        # 请求购物车页
        print u'购物车页'
        response = self.session.get('/cart.html?c=cart&a=load')
        # print response

        # 效验添加商品是否在购物车中
        data = json.loads(response['body'])
        cart_info = data['data']['cart_info']
        goodsIds = {}
        activitys = cart_info['activitys']
        for item in activitys:
            if 'goods' not in item:
                continue
            for goods in item['goods']:
                if 'goods_id' not in goods:
                    continue
                goods_number = int(goods['goods_number'])
                goodsIds[int(goods['goods_id'])] = goods_number
        self.assertTrue(goodsId in goodsIds.keys(), u'添加的商品不在购物车中')


        # 请求订单确认页
        print u'订单确认页'
        if sales == 0 and status != 1:
            return (False, '')
        param = {'goods[0][id]': str(goodsId), 'goods[0][number]':'1'}
        response1 = self.session.get('/checkout.html?rp=goods_detail&rl=checkout' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)
        # print response1['body']

        
        '''
        判断: 游客身份跳转到登录页面
        '''
        if response1['body'].find('js/login.js') != -1:
            return (True, response1['body'])

        # 订单页取出addressId,获取addressId的值
        value = 'window.addressId = '
        index = response1['body'].find(value)
        if index == -1:
            return (False, '')
        # print index
        add_index = index + len(value)
        for i in response1['body'][add_index:]:
            if i == ';':
                break
            add_index += 1
        # print response1['body'][(index+len(value)):add_index]
        addressId = response1['body'][(index+len(value)):add_index]
        print addressId


        # 请求订单确认页，设置不使用红包
        param = {'bonus_id':0}
        response = self.session.get('/checkoutBonus.html?' + urllib.urlencode(param))
        print urllib.urlencode(param)
        # print response
        result = False


        # 去支付,请求vode页
        print u'订单确认页生成订单'
        param = {'order_id':0, 'bonus_id':0, 'address_id':addressId, 'commission':0}
        response = self.session.get('/vdone.html?rp=checkout&rl=next' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)
        print response['body']

        return True

    
    # =============执行case==============
    def test_01_seller_timeShop_getCart_buy(self):
        print u'卖家身份: 登录 -> 首页限时购 -> [随机限时购商品] -> 商品详情页 -> 加入购物车 -> 订单确认 -> 去支付生成订单'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_timeShop_getCart_buy()
        self.assertTrue(ret)

    
    def test_02_user_timeShop_getCart_buy(self):
        print u'买家身份: 登录 -> 首页限时购 -> [随机限时购商品] -> 商品详情页 -> 加入购物车 -> 订单确认 -> 去支付生成订单'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_timeShop_getCart_buy()
        self.assertTrue(ret)

    
    def test_03_no_timeShop_getCart_buy(self):
        print u'游客身份: 首页限时购 -> [随机限时购商品] -> 商品详情页 -> 加入购物车 -> 订单确认 -> 登录(判断是否跳到登录页)'
        ret = self.action_timeShop_getCart_buy()
        print ret
        # 取出游客sess_key
        sess_key = self.session.session
        print sess_key

                
