#!/usr/bin/env python
# -*- coding:utf-8 -*-

# test_case_login_getPageFirst_loginout.py  登录 -> 首页（首页第一屏、搜索、菜单、首页猜你喜欢） -> 退出登录 ===


import requests
import unittest
import urllib,urllib2
import csv
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from requests.sessions import Session
from nose.tools import *
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv


# 创建测试
class homePage(unittest.TestCase):

    users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')
    '''
    # 读取test_user.csv
    def load(self):
        self.user = []
        with open("/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv", "rb") as fd:
            reader = csv.reader(fd)
            print reader
            for arr in reader:
                self.user.append({'mobile': arr[0], 'password':arr[1]})

    # 取出test_user.csv文件
    def randUser(self):
        self.load()
        return self.user
    '''


    # ===================执行case===============
    def setUp(self):
        print u'=======测试开始======'
        # self.load()
        # self.users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')
        #self.datafile.loadCsv()
        #self.datafile.randCsv()

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'=======测试结束======'
        self.session.api('/api/mg/auth/user/logout')

    
    # =======================测试case===========================
    def action_pageFirst(self):
        # 请求首页第一屏接口
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')
        # self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        # 请求首页搜索接口
        print u'首页搜索'
        data = self.session.api('/api/mg/sale/index/getSearch')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        # 请求首页菜单接口
        print u'首页菜单'
        data = self.session.api('/api/mg/sale/index/getMenu')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        # 请求首页第二屏(猜你喜欢)
        print u'首页第二屏(猜你喜欢)'
        data = self.session.api('/api/mg/sale/index/getPageSecond')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)
        return True         # 不return,下面执行报错None

    
    def test_01_seller_pageFirst(self):
        print u'卖家身份: 登录 -> 首页(首页第一屏、首页搜索、首页菜单、首页猜你喜欢) -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        # ipdb.set_trace()
        ret = self.action_pageFirst()
        self.assertTrue(ret)
        
    
    def test_02_user_pageFirst(self):
        print u'买家身份: 登录 -> 首页(首页第一屏、首页搜索、首页菜单、首页猜你喜欢) -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_pageFirst()
        self.assertTrue(ret)
        

    def test_03_no_pageFirst(self):
        print u'游客身份: 登录 -> 首页(首页第一屏、首页搜索、首页菜单、首页猜你喜欢) -> 退出登录'
        # self.session.api('/api/mg/auth/user/login', self.user[1])
        ret = self.action_pageFirst()
        self.assertTrue(ret)
        # self.assertTrue(not ret, "not login user failed!") 