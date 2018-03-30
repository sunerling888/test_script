#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''test_case_06_login_firstGuess_goodsDetail_loginout.py    登录 -> 首页(第一屏) -> 首页(猜你喜欢) ->[随机选择猜你喜欢列表商品id] -> 商品详情页 -> 退出登录 '''


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
class firstGuess_goodsDetail(unittest.TestCase):

    '''获取user_csv文件'''
    users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')


    # =====执行测试=====
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')

    
    # ============测试case================
    def action_firstGuess_goodsDetail(self):

        # 请求首页第一屏
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')
        self.assertEqual(int(data['code']), 0, data['data'])

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
                # print (data['command']['content'])
                if not data.has_key('command'):
                    continue
                if not data['command'].has_key('content'):
                    continue
                if re.match(r'^/\d+.html', data['command']['content']):
                    contents.append(data['command']['content'])
            # print contents

            length = len(contents)
            # print length

            randIndex = random.randint(0, length - 1)
            content = contents[randIndex]
            # print "content:%s" %(content)

            goodsIdurl = contents[randIndex]
            goodsId = re.findall(r"\d+\d*", goodsIdurl)[0]
            print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)

            # self.assertEqual(int(data['code']), 0, data['data'])
            # print json.dumps(data)

            # 请求商品详情页
            print u'商品详情页'
            print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
            param = {'goodsId': goodsId}
            data = self.session.api('/api/mg/good/info/detail', param)
            # print json.dumps(data)
            return True


    # =============执行case===============
    def test_01_seller_firstGuess_goodsDetail(self):
        print u'卖家身份:登录 -> 首页(第一屏) -> 首页(猜你喜欢) ->[随机选择猜你喜欢列表商品id] -> 商品详情页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        ret = self.action_firstGuess_goodsDetail()
        # print ret
        self.assertTrue(ret)

    
    def test_02_user_firstGuess_goodsDetail(self):
        print u'买家身份:登录 -> 首页(第一屏) -> 首页(猜你喜欢) ->[随机选择猜你喜欢列表商品id] -> 商品详情页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        ret = self.action_firstGuess_goodsDetail()
        self.assertTrue(ret)

    
    def test_03_no_firstGuess_goodsDetail(self):
        print u'游客身份:登录 -> 首页(第一屏) -> 首页(猜你喜欢) ->[随机选择猜你喜欢列表商品id] -> 商品详情页 -> 退出登录'
        #self.session.api('/api/mg/auth/user/login')

        ret = self.action_firstGuess_goodsDetail()
        self.assertTrue(ret)
        




