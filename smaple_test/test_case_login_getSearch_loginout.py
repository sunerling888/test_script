#!/usr/bin/env python
# -*- coding:utf-8 -*-

# test_case_login_Search_loginout.py  登录 -> 首页（第一屏、猜你喜欢） -> 搜索(建议词、热词、搜索结果) -> 退出登录 


import requests
import unittest
import urllib, urllib2
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
class Search(unittest.TestCase):

    users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')

    # ===========执行测试=============
    def setUp(self):
        print u'=====测试开始====='

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'=====测试结束====='
        self.session.api('/api/mg/auth/user/logout')

    
    # ==============测试case===============
    def action_Search(self, user=None):
        
        # 请求首页第一屏接口
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')
        self.assertEqual(int(data['code']), 0, data['data'])
        print json.dumps(data)

        # 请求首页第二屏（猜你喜欢）
        print u'首页第二屏(猜你喜欢)'
        data = self.session.api('/api/mg/sale/index/getPageSecond')
        self.assertEqual(int(data['code']), 0, data['data'])
        print json.dumps(data)
       
        # 请求搜索建议词接口
        print u'搜索建议词'
        # q:需要带的参数
        param = {'q' : user['q']}
        # print user
        data = self.session.api('/api/mg/sale/search/suggestKeywords', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        # 取出keywords
        keywords = data['data']['keywords']
        # 判断是否有结果；有返回Ture，否则返回False
        if user['expect'] == "true":
            self.assertTrue(keywords)
            for item in keywords:
                self.assertTrue(user['q'] in item)
        else:
            self.assertTrue(not keywords)
        print json.dumps(data)
        
        # 请求搜索热词
        print u'搜索热词'
        data = self.session.api('/api/mg/sale/search/getHotwords')
        self.assertEqual(int(data['code']), 0, data['data'])
        print json.dumps(data)
        # return True
        
        # 请求搜索结果
        print u'搜索结果'
        data = self.session.api('/api/mg/sale/search/getGoods')
        self.assertEqual(int(data['code']), 0, data['data'])
        print json.dumps(data)
        return True


    # ==========执行case===============
    def test_01_seller_Search(self):
        print u'卖家身份: 登录 -> 首页(第一屏,第二屏[猜你喜欢]) -> 搜索建议词 -> 搜索热词 -> 搜索结果'
        user = self.users.next()  #上面"搜索建议词"已经调用过user,这里再调用就会出现取第二个数据
        # param = self.user.next()
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_Search(user)
        self.assertTrue(ret)
    
    def test_02_user_Search(self):
        print u'买家身份: 登录 -> 首页(第一屏,第二屏[猜你喜欢]) -> 搜索建议词 -> 搜索热词 -> 搜索结果'
        user = self.users.next()
        # print "TEST2"
        # print user
        # return
        self.session.api('/api/mg/auth/user/login', user)
        ret = self.action_Search(user)
        self.assertTrue(ret)
        
    '''
    def st_03_no_Search(self):
        print u'游客身份: 登录 -> 首页(第一屏,第二屏[猜你喜欢]) -> 搜索建议词 -> 搜索热词 -> 搜索结果'
        # user = self.users.current()
        # print user
        ret = self.action_Search()
        self.assertTrue(ret）
    '''
        
        