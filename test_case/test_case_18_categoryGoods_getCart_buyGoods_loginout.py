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

        # 请求分类页(图书11-14岁)
        print u'分类页(图书11-14岁)'
        response = self.session.get('/categorySync-8-444-2.html?sort=2&_t=1523329035375.4707&page_size=10&page=1')
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
        # print response1

        # 订单确认页设置不使用红包
        param = {'bonus_id':0}
        response = self.session.get('/checkoutBonus.html?' + urllib.urlencode(param))
        print urllib.urlencode(param)
        #print response

        # 订单页取出addressId
        result = False
        soup = BeautifulSoup(response1['body'], 'html.parser')
        print soup
        content = soup.find_all("script", class_="window.addressId") 
        print content
        # 获取addressId里的值
        '''
        if len(content) > 0:
        content = content[0].get_text()

        print "content*****************"
        content
        print "content*****************"
        # print response['body']
        '''
        return (result, response1['body']) 
          
        # 点击去支付,请求vdone页
        # print u'订单确认页生成订单'
        
        return True

    # =============执行case==============
    def test_01_seller_categoryGoods_getCart_buy(self):
        print u'卖家身份:'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_categoryGoods_getCart_buy()
        self.assertTrue(ret)