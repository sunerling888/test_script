#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_18_categoryGoods_getCart_buyGoods_loginout.py
登录 -> 分类页 -> 商品详情页 -> 加入购物车 -> 购物车结算 -> 订单确认页 -> 去支付
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
from bs4 import BeautifulSoup


# 创建测试
class categoryGoods_getCart_buy(unittest.TestCase):

    '''获取test_user.csv'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')


    # ========执行测试==========
    def setUp(self):
        print u'-----测试开始-----'

        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')

    

    # ===================测试case====================
    def action_categoryGoods_getCart_buy(self, goods_Id=None):

        # 请求分类页(图书0-2岁)
        print u"分类页(图书0-2岁)"
        response = self.session.get('/categorySync-8-14-2.html?sort=2&_t=1522657956463.7556&page_size=10&page=1')
        # print response
        # 取出good_id,随机good_id
        body = response['body']

        body = json.loads(body)
        goodIds = []
        if not body.has_key('data'):
            return (False, '')
        for item in body['data']:
            goodIds.append(int(item['goods_id']))
        print goodIds

        # 随机goods_id
        length = len(goodIds)
        randIndex = random.randint(0, length - 1)
        goodsId = goodIds[randIndex]
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)


        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId':goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
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


        # 请求购物车页面
        print u'购物车页面'
        response = self.session.get('/cart.html?c=cart&a=load')
        # print response
        # 校验购物车页面是否在购物车中
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
        self.assertTrue(goodsId in goodsIds.keys(), u'添加商品不在购物车中')


        # 点击结算,请求订单确认页
        print u'订单确认页'
        if sales == 0 and status != 1:
            return (False, '')
        param = {'goods[0][id]': str(goodsId), 'goods[0][number]': '1'}
        response1 = self.session.get('/checkout.html?rp=goods_detail&rl=checkout' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)
        # print response1['body']

        # 判断:游客身份跳转到登录页面
        if response1['body'].find('js/login.js') != -1:
            return (True, response1['body'])

        # 订单页取出addressId,获取addressId的值
        value = 'window.addressId = '
        index = response1['body'].find(value)
        if index == -1:
            return (False, '')
        # print index
        add_index = index+len(value)
        for i in response1['body'][add_index:]:
            if i == ';':
                break
            add_index += 1
        # print response1['body'][(index+len(value)):add_index]
        addressId = response1['body'][(index+len(value)):add_index]
        print addressId

        # 订单确认页设置不使用红包
        param = {'bonus_id':0}
        response = self.session.get('/checkoutBonus.html?' + urllib.urlencode(param))
        print urllib.urlencode(param)
        # print response
        result = False
        # return (result, response1['body']) 
          
        # 点击去支付,请求vdone页
        print u'订单确认页生成订单'
        # http://18600967174.davdian.com/vdone.html?rp=checkout&rl=next&order_id=0&bonus_id=0&address_id=3652798&password=&commission=0&rp=cart&rl=checkout
        param = {'order_id':0, 'bonus_id':0, 'address_id':addressId, 'commission':0}
        response = self.session.get('/vdone.html?rp=checkout&rl=next' + '&' + urllib.urlencode(param))
        print urllib.urlencode(param)
        print response['body']
        '''
        # 效验status值是否等于0
        body = response['body']
        statuss = []
        if not body.has_key('status'):
            return (False, '')
        if len(body['status']) < 0:
            return (False, '')
        print status
        '''
        # 效验status是否等于0,不等于0打印status,msg
        s = json.loads(response['body'])
        if 'status' in s:
            if s['status'] != 0:
                print "Failed! [status not 0][status:%s][message:%s]" % (s['status'], s['msg'])
                # response.("Failed! [status not 0][status:%s][message:%s]" % (s['status'], s['msg']))
                return False
                
            print "SUCEESS! [status not 0][status:%s][message:%s]" % (s['status'], s['msg'])
        return True

    # =============执行case==============
    def test_01_seller_categoryGoods_getCart_buy(self):
        print u'卖家身份: 登录 -> 分类页 -> 商品详情页 -> 加入购物车 -> 购物车结算 -> 订单确认页 -> 去支付'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_categoryGoods_getCart_buy()
        self.assertTrue(ret)

    
    def test_02_user_categoryGoods_getCart_buy(self):
        print u'买家身份: 登录 -> 分类页 -> 商品详情页 -> 加入购物车 -> 购物车结算 -> 订单确认页 -> 去支付'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_categoryGoods_getCart_buy()
        self.assertTrue(ret)

    
    def test_03_no_categoryGoods_getCart_buy(self):
        print u'游客身份: 分类页 -> 商品详情页 -> 加入购物车 -> 购物车结算 -> 订单确认页 -> 登录(判断是否跳到登录页)'
        ret= self.action_categoryGoods_getCart_buy()
        print ret
        # 取出sess_key
        sess_key = self.session.session
        print sess_key

        self.assertTrue(ret)
    