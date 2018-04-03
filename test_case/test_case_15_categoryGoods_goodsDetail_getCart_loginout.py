#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''test_case_15_searchGoods_goodsDetail_getCart_loginout.py
登录 -> 分类 -> [随机取商品id] -> 商品详情页 -> 加入购物车 -> 购物车(增删查改) -> 退出登录【卖家/买家/游客】
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
class categoryGoods_getCart(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    # goods = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_goods_cart.csv')

    # ========执行测试==========
    def setUp(self):
        print u'-----测试开始-----'

        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')


        
    # ===================测试case====================
    def action_categoryGoods_getCart(self, goods_Id=None):

        
        # 请求分类页(图书0-2岁)
        print u"分类页(图书0-2岁)"
        response = self.session.get('/categorySync-8-14-2.html?sort=2&_t=1522657956463.7556&page_size=10&page=1')
        # data = json.loads(response['body'])
        # print response
        # 取出good_id,随机goods_id
        body = response['body']
        
        body = json.loads(body)
        goodIds = []
        # if 'data' not in body['data']:
            # return False
        if not body.has_key('data'):    # 判断body中的key:data
            return False
        for item in body['data']:       # 遍历key:data
            # if 'data' not in item:
                # continue
            # if len(item['data']) < 1 or 'goods_id' not in item['data'][0]:
                # continue
            # print item['data'][0]['goods_id']
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
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        self.assertEqual(int(data['code']), 0, data['data'])


        # 添加购物车
        print u'添加购物车'
        param = {'goods': urllib.quote(json.dumps({"number":1, "goods_id":goodsId}))}
        # data_param = urllib.quote(json.dumps({"number":1, "goods_id":goodsId}));
        # print data_param
        print param['goods']
        data = self.session.post('/index.php?c=cart&a=add_to_cart&m=default', urllib.urlencode(param))
        #data = self.session.post('/index.php?c=cart&a=add_to_cart', 'goods=%257B%2522number%2522%253A%25201%252C%2520%2522goods_id%2522%253A%2520%2522562128%2522%257D')
        print data

        
        # 请求购物车页面
        print u'购物车页面'
        response = self.session.get('/cart.html?c=cart&a=load')
        # print response
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
                goods_number = int(goods["goods_number"])
                goodsIds[int(goods['goods_id'])] = goods_number
        self.assertTrue(goodsId in goodsIds.keys(), u'添加商品不在购物车中')


        # 修改商品数量+1
        print u'购物车添加商品数量'
        # params = {'goodsId': goodsId}
        param = {'goods[' + str(goodsId) + '][act_id]':'0', 'goods[' + str(goodsId) + '][goods_id]': str(goodsId), 'goods[' + str(goodsId) + '][goods_number]':'2', 'goods[' + str(goodsId) + '][editCheck]':'false', 'goods[' + str(goodsId) + '][price_act_id]':'0', 'goods[' + str(goodsId) + '][price_act_type]':'0' }
        print urllib.urlencode(param)
        data = self.session.post('/index.php?c=cart&a=change', urllib.urlencode(param))
        print data
        

        # 效验添加的商品数量
        body = data['body']
        new_goodsIds= {}
        body = json.loads(body)

        if not body.has_key('data'):
            return False
        cart_info = body['data']['cart_info']
        # body = response['body']
        # body = json.loads(body)
        # print body
        
        activitys = cart_info['activitys']
        for item in activitys:
            if 'goods' not in item:
                continue
            for goods in item["goods"]:
                if 'goods_id' not in goods:
                    continue
                goods_number = int(goods["goods_number"])
                new_goodsIds[int(goods["goods_id"])] = goods_number

        print "new goods_number: %d" % new_goodsIds.get(goodsId, 0)
        print "goods_number: %d" % goodsIds.get(goodsId, 0)
        self.assertTrue((new_goodsIds.get(goodsId, 0) - goodsIds.get(goodsId, 0))==1, u"商品数量不正确")
        

        # 修改商品数量-1
        
        return True

        


    # =============执行case===============
    def test_01_seller_categoryGoods_getCart(self):

        print u'卖家身份:'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        #goods_Id = self.goods.random()
        ret = self.action_categoryGoods_getCart()
        self.assertTrue(ret)
