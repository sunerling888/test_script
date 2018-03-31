#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''test_case_09_login_groupList_goodsDetail_loginout.py   登录 -> 首页（第一屏/猜你喜欢）-> 组团列表 -> 【随机选择组团列表商品id】 -> 商品详情页 -> 退出登录【卖家/买家/游客】'''


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
class groupList_goodsDetail(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_user.csv')
    '''获取test_groupList.csv文件'''
    groups = ReaderCsv('/Users/dabenchen/Downloads/daben_chen_py/test_data/test_groupList.csv')

    # =====执行测试======
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')

    

    # ==============测试case==================
    '''以下是: 登录 -> 首页(第一屏/猜你喜欢) -> 组团[随机选择组团列表页商品id] -> 商品详情页 -> 退出登录【卖家/买家/游客】'''
    def action_groupList_goodsDetail(self, group_list=None):

        # 请求首页第一屏
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')
        # self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)


        # 请求首页猜你喜欢
        print u'首页猜你喜欢'
        data = self.session.api('/api/mg/sale/index/getPageSecond')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)


        # 请求组团团购精选接口
        print u'组团列表'
        # print group_list
        print "DEBUG\t[%s][%s]" % (u'group_list', group_list)
        param = {'reverseType': group_list['reverseType'], 'pageIndex': group_list['pageIndex']}
        data = self.session.api('/api/mg/sale/reverse/getList', param)

        '''随机选择组团列表商品id'''

        reverseGroup = data['data']['reverseGroup']
        goodsIds = []
        dataList = reverseGroup['dataList']
        for item in dataList:
            goodsIds.append((int)(item['goodsId']))

        length = len(goodsIds)
        print length
        randIndex = random.randint(0, length - 1)

        goodsId = goodsIds[randIndex]
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)

        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)


        # 请求商品详情页
        print u'商品详情页'
        # print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)
        return True

    
    # ============执行case===============
    def test_01_seller_groupList(self):
        print u'卖家身份: 登录 -> 首页（第一屏/猜你喜欢）-> 组团列表 -> 【随机选择组团列表商品id】 -> 商品详情页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        
        
        group_list = self.groups.random()
        ret = self.action_groupList_goodsDetail(group_list)
        self.assertTrue(ret)

    
    def test_02_user_groupList(self):
        print u'买家身份: 登录 -> 首页（第一屏/猜你喜欢）-> 组团列表 -> 【随机选择组团列表商品id】 -> 商品详情页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)

        group_list = self.groups.random()
        ret = self.action_groupList_goodsDetail(group_list)
        self.assertTrue(ret)

    
    def test_03_no_groupList(self):
        print u'游客身份: 登录 -> 首页（第一屏/猜你喜欢）-> 组团列表 -> 【随机选择组团列表商品id】 -> 商品详情页 -> 退出登录'
        # self.session.api('/api/mg/auth/user/login')

        group_list = self.groups.random()
        ret = self.action_groupList_goodsDetail(group_list)
        self.assertTrue(ret)

    
        

    