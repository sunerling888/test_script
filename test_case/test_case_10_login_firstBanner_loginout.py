#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''test_case_10_login_firstBanner_loginout      # 登录 -> 首页（第一屏/猜你喜欢）-> 首页banner图 -> 【随机选择banner专题】 -> 专题页 -> 退出登录【卖家/买家/游客】'''


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
class firstBanner(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')



    # =====执行测试======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')

    
    # ==============测试case==================
    '''以下是: 登录 -> 首页（第一屏/猜你喜欢）-> 首页banner图 -> 【随机选择banner专题】 -> 专题页 -> 退出登录'''
    def action_firstBanner(self, topic_Id=None):

        # 请求首页第一屏
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')
        # self.assertEqual(int(data['code']), 0, data['data'])
        

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
                m = re.match(r'^/.+\?topicId=(\d+)&', data['command']['content'])
                if m:
                    topicId = m.group(1)
                    contents.append(topicId)
        print "DEBUG\t[%s][%s]" % (u'contents', contents)

        length = len(contents)
        print "DEBUG\t[%s][%s]" % (u'length', length)

        randIndex = random.randint(0, length - 1)
        topicId = contents[randIndex]

        # topicIdurl = contents[randIndex]
        # topicId = re.findall(r"\d+\d*", topicIdurl)[0]
        print "DEBUG\t[%s][%s]" % (u'topicId', topicId)
        # print json.dumps(data)

        
        # 请求首页猜你喜欢
        print u'首页猜你喜欢'
        data = self.session.api('/api/mg/sale/index/getPageSecond')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)
        # return True


        # 请求首页banner专题页
        print u'首页banner专题页'
        param = {'topicId': topicId}
        data = self.session.api('/api/mg/sale/topic/getTopicInfo', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)
        return True
        


    # =============执行case===============
    def test_01_seller_firstBanner(self):
        print u'卖家身份: 首页（第一屏/猜你喜欢）-> 首页banner图 -> 【随机选择banner专题】 -> 专题页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        
        ret = self.action_firstBanner()
        self.assertTrue(ret)

    
    def test_02_user_firstBanner(self):
        print u'买家身份: 首页（第一屏/猜你喜欢）-> 首页banner图 -> 【随机选择banner专题】 -> 专题页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        ret = self.action_firstBanner()
        self.assertTrue(ret)

    
    def test_03_no_firstBanner(self):
        print u'游客身份: 首页（第一屏/猜你喜欢）-> 首页banner图 -> 【随机选择banner专题】 -> 专题页 -> 退出登录'
        # self.session.api('/api/mg/auth/user/login')

        ret = self.action_firstBanner()
        self.assertTrue(ret)






