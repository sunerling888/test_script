#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''test_case_login_timeShop_goodsDetail_loginout.py    登录 -> 首页(第一屏) ->[随机选择限时购列表商品id] -> 商品详情页 -> 退出登录 '''


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
class timeShop_goodsDetail(unittest.TestCase):

    '''获取user_csv文件'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')


    # =====执行测试=====
    def setUp(self):
        print u'------测试开始------'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束------'
        self.session.api('/api/mg/auth/user/logout')


    # ============测试case================
    '''以下是:登录 -> 首页(第一屏) ->[随机选择限时购列表商品id] -> 商品详情页 -> 退出登录'''
    def action_timeShop_goodsDetail(self):
        
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
        # self.assertEqual(int(data['code']), 0, data['data']
        # print json.dumps(data)
        

        # 请求首页猜你喜欢
        print u'首页猜你喜欢'
        data = self.session.api('/api/mg/sale/index/getPageSecond')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)
        
        
        # 请求商品详情页
        print u'商品详情页'
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        # print data
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)
        return True


    # =============执行case===============
    def test_01_seller_timeShop_goodsDetail(self):
        print u'卖家身份:登录 -> 首页(第一屏) ->[随机选择限时购列表商品id] -> 商品详情页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        
        ret = self.action_timeShop_goodsDetail()
        # print ret
        self.assertTrue(ret)

    
    def test_02_user_timeShop_goodsDetail(self):
        print u'买家身份:登录 -> 首页(第一屏) ->[随机选择限时购列表商品id] -> 商品详情页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        ret = self.action_timeShop_goodsDetail()
        self.assertTrue(ret)


    def test_03_no_timeShop_goodsDetail(self):
        print u'游客身份:登录 -> 首页(第一屏) ->[随机选择限时购列表商品id] -> 商品详情页 -> 退出登录'
        #self.session.api('/api/mg/auth/user/login')

        ret = self.action_timeShop_goodsDetail()
        self.assertTrue(ret)

