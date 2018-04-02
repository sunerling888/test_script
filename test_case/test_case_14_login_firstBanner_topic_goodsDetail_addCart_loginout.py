#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''
test_case_14_login_firstBanner_topic_goodsDetail_addCart_loginout.py
登录 -> 新专题 -> 【随机选择商品id】-> 商品详情页 -> 加入购物车 -> 效验购物车 -> 退出登录【卖家/买家/游客】
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
class firstBanner_addCart(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    # users = ReaderCsv('/home/xiaoqiang.li/scripts/release_li/test_api_dvd/test_data/test_user.csv')
    topics = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_topic.csv')

    # =====执行测试======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')



    # ==============测试case===================
    '''以下是: 新专题 -> 【随机选择商品id】-> 商品详情页 -> 加入购物车 -> 效验购物车 -> 退出登录【卖家/买家/游客】'''
    def action_firstBanner_addCart(self, topic_Id=None):
          
        # 请求首页banner专题页
        print u'首页banner专题'
        print topic_Id
        param = {'topicId': topic_Id['topicId']}
        data = self.session.api('/api/mg/sale/topic/getTopicInfo', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        
        # print json.dumps(data)
        # print type(data)

        
        # 取出专题页goodsId
        topicContent = data['data']['topicContent']
        # print type(topicContent)
        # 返回的是字符串，先loads转换成对象
        topicContent = json.loads(topicContent)
        print type(topicContent)
        # print type(topicContent)
        # 取下标第4个
        # print topicContent['list'][4]
        goodsIds = []
        goods_Ids = topicContent['list'][4]['goods']
        # 转换成数组list
        goodsIds = goods_Ids.split(',')
        print goodsIds

        # 随机list
        length = len(goodsIds)
        randIndex = random.randint(0, length - 1)
        goodsId = goodsIds[randIndex]
        print goodsId
        
        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        
        
        # 添加购物车
        print u'添加购物车'
        # 添加购物车的接口，需要goods: {"number":1,"goods_id":"550358"},用urllib.quote的方式
        param = {'m': 'default', 'c': 'cart', 'a': 'add_to_cart', 'goods': urllib.quote(json.dumps({"number":1, "goods_id":goodsId}))}
        print param['goods']
        data = self.session.post('/cart.html', urllib.urlencode(param))
        print data


        # 请求购物车页面
        print u'购物车页面'
        response = self.session.get('/cart.html')
        # 请求购物车接口
        print u'购物车接口'
        response = self.session.get('/cart.html?c=cart&a=load')
        # print response

        data = json.loads(response['body'])

        cart_info = data['data']['cart_info']
        goodsIds = {}
        activitys = cart_info['activitys']
        for item in activitys:
            if 'goods' not in item:
                continue

            for goods in item["goods"]:
                if 'goods_id' not in goods:
                    continue
                goods_number = int(goods["goods_number"])
                goodsIds[int(goods['goods_id'])] = goods_number
                # goodsIds.append((int)(goods['goods_id']))
        # print goodsId
        # print goodsIds
        # self.assertTrue(goodsId in goodsIds.keys(), u"商品不在购物车中")
        return True
        

    # =============执行case===============
    def test_01_seller_firstBanner_addCart(self):
        print u'卖家身份: 新专题 -> 【随机选择商品id】-> 商品详情页 -> 加入购物车 -> 效验购物车 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        topic_Id = self.topics.random()
        ret = self.action_firstBanner_addCart(topic_Id)
        self.assertTrue(ret)


    def test_02_user_firstBanner_addCart(self):
        print u'买家身份: 新专题 -> 【随机选择商品id】-> 商品详情页 -> 加入购物车 -> 效验购物车 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        topic_Id = self.topics.random()
        ret = self.action_firstBanner_addCart(topic_Id)
        self.assertTrue(ret)

    
    def test_03_no_firstBanner_addCart(self):
        print u'游客身份: 新专题 -> 【随机选择商品id】-> 商品详情页 -> 加入购物车 -> 效验购物车 -> 退出登录'
        topic_Id = self.topics.random()
        ret = self.action_firstBanner_addCart(topic_Id)
        self.assertTrue(ret)
