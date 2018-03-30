#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''test_case_login_getGoodsdetail_loginout.py    登录 -> 首页（随机取限时购/猜你喜欢商品） -> 商品详情页 '''


import requests
import unittest
import urllib,urllib2
import csv
import json
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv


# 创建测试
class getGoodsdetail(unittest.TestCase):

    '''获取csv文件'''
    users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')


    # =====执行测试=====
    def setUp(self):
        print u'------测试开始------'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束------'


    # ============测试case================
    '''以下是:首页(第一屏、猜你喜欢) -> 随机取出商品id -> 各自商品详情页'''
    def action_Detail(self):

        # 请求首页第一屏
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')
        # 取feedList    
        feedList = data['data']['feedList']   
        # 设定goodsIds
        goodsIds = []
        # 遍历feedList
        for item in feedList:
            if 'body' not in item or 'dataList' not in item['body']:
                continue
            
            if len(item['body']['dataList']) < 1 or 'goodsId' not in item['body']['dataList'][0]:
                continue
            
            goodsIds.append((int)(item['body']['dataList'][0]['goodsId']))
        
        
        # 最后包含了，所以要length - 1
        length = len(goodsIds)
        randIndex = random.randint(0, length - 1)
        
        # 随机取goodsid,还包含了一层['body']['dataList']
        #goodsidIndex = random.randint(0, len(feedList[randIndex]['body']['dataList']) - 1)
        #print feedList[randIndex]
        # 给定一个goodsId,判断，因为feedList里前几个没有goodsId
        goodsId = goodsIds[randIndex]

        # 取出goodsid
        # goodsId = int(data['data']['feedList'][]['body']['dataList']['goodsId'])
        print goodsId
        
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        # 请求商品详情页
        print u'商品详情'
        print goodsId
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        # print data
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)
        return True


    # =============执行case===============
    def test_01_seller_getGoodsdetail(self):
        print u'卖家身份:登录 -> 首页（随机取限时购/猜你喜欢商品） -> 商品详情页'
        user = self.users.next()

        self.session.api('/api/mg/auth/user/login', user)
        
        ret = self.action_Detail()
        # print ret
        self.assertTrue(ret)
