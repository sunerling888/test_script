#!/usr/bin/env python
# -*- coding:utf-8 -*-

# test_case_login_loginout.py  === 登录 -> 个人中心 -> 设置页面 -> 退出登录 ===


import requests
import unittest
import hashlib
from requests.sessions import Session
import urllib2
import urllib
import csv
import sys
from nose.tools import *
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from lib.davdianSession import DavdianSession
from lib.davdianCsv import ReaderCsv


# 创建测试
class Login(unittest.TestCase):

    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')

    '''
    idx = 0
    user = []

    # 读取test_user.csv文件
    def load(self):
        # print "Load"
        self.user = []
        with open("/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv", "rb") as fd:
            reader = csv.reader(fd)
            print reader
            for arr in reader:
                self.user.append({'mobile': arr[0], 'password': arr[1]})

    # 取出test_user.csv文件
    def randUser(self):
        self.load()
        return self.user
    '''

    # ====================执行case====================
    def setUp(self):
        print u'=======测试开始======'
        print self.users
        # self.load()
        # 方式一
        # user = self.randUser()
        # self.session = DavdianSession(user['mobile'], user['password'])
        # self.users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')
        # 方式二
        self.session = DavdianSession()
        #self.session.api('/api/mg/auth/user/login', {'mobile': arr['mobile'], 'password': arr['password']})
        #self.test_01_login_success()

    def tearDown(self):
        print u'=======测试结束======'
        self.session.api('/api/mg/auth/user/logout')


    # =======================测试case===========================
    def action_setting(self):
        print u'个人中心接口'
        data = self.session.api('/api/mg/user/center/index')
        self.assertEqual(int(data['code']), 0, data['data'])
        print data['code']
        # print json.dumps(data)      # 打印详细输出log


        # 请求设置页面
        print u'设置页面'
        response = self.session.get('/settings.html')
        # print response
        return "退出登录" in response['body']



    def test_01_seller_setting(self):
        print u'卖家身份: 登录 -> 个人中心 -> 设置页面 -> 退出登录'
        user = self.users.next()
        # print user
        # return
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_setting()
        self.assertTrue(ret)


    def test_02_user_setting(self):
        print u'买家身份: 登录 -> 个人中心 -> 设置页面 -> 退出登录'
        user = self.users.next()
        # print user
        # return
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_setting()
        self.assertTrue(ret)


    def test_03_no_setting(self):
        print u'游客身份: 登录 -> 个人中心 -> 设置页面 -> 退出登录'
        ret = self.action_setting()
        self.assertTrue(not ret, "not login user failed!")






