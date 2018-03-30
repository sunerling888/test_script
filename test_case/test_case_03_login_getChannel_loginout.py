#!/usr/bin/env Python
# -*- coding:utf-8 -*-

'''test_case_login_getChannel_loginput.py  登录 -> 首页（第一屏、猜你喜欢） -> 二级菜单(第一屏、猜你喜欢) -> 退出登录  -[卖家、买家、游客]'''


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
class getChannel(unittest.TestCase):

    '''获取csv文件'''
    users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')
    menus = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_menu.csv')

    # ========执行测试==========
    def setUp(self):
        print u'-----测试开始------'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束------'

    
    # ========测试case==========
    '''以下是:首页（第一屏、猜你喜欢） -> 二级菜单(第一屏、猜你喜欢) -> 退出登录'''
    def action_Channel(self, menu_id=None):
        
        # 请求首页第一屏
        print u'首页第一屏'
        data = self.session.api('/api/mg/sale/index/getPageFirst')
        # self.assertEqual(int(data['code']), 0, data['data'])
        # print data['code']
        # print json.dumps(data)

        # 请求首页第二屏(猜你喜欢)
        print u'首页第二屏(猜你喜欢)'
        data = self.session.api('/api/mg/sale/index/getPageSecond')
        self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)
        
        # 请求二级页第一屏
        print u'二级页第一屏'
        # 需要上传参数:menuId
        print menu_id
        param = {'menuId': menu_id['menuId']}
        data = self.session.api('/api/mg/sale/channel/getPageFirst', param)
        # self.assertEqual(int(data['code']), 0, data['data'])
        # print json.dumps(data)

        # 请求二级页猜你喜欢
        print u'二级页猜你喜欢'
        print menu_id
        param = {'menuId': menu_id['menuId'], 'pageIndex': menu_id['pageIndex']}
        # 设置页数
        currentPage = 1
        # lastPage(标识是否还有下一页)
        lastPage = 0
        while lastPage == 0:
            param['pageIndex'] = currentPage

            # 打印页数
            print "REQUEST PAGE %s" % currentPage
        
            data = self.session.api('/api/mg/sale/channel/getGuessBody', param)
            # print data
            lastPage = int(data['data']['feedList'][0]['body']['lastPage'])
            print ('lastPage', lastPage)

            # 页数+1
            currentPage += 1
            self.assertEqual(int(data['code']), 0, data['data'])
            # print json.dumps(data)
            return True


    # ============执行case===============
    def test_01_seller_getChannel(self):
        print u'卖家身份:登录 -> 首页（第一屏、猜你喜欢） -> 二级菜单(第一屏、猜你喜欢) -> 退出登录'
        user = self.users.next()

        self.session.api('/api/mg/auth/user/login', user)
        menu_id = self.menus.random()
        ret = self.action_Channel(menu_id)
        self.assertTrue(ret)

    def test_02_user_getChannel(self):
        print u'买家身份:登录 -> 首页（第一屏、猜你喜欢） -> 二级菜单(第一屏、猜你喜欢) -> 退出登录'
        user = self.users.next()

        self.session.api('/api/mg/auth/user/login', user)
        menu_id = self.menus.random()
        ret = self.action_Channel(menu_id)
        self.assertTrue(ret)

    def test_03_no_getChannel(self):
        print u'游客身份:登录 -> 首页（第一屏、猜你喜欢） -> 二级菜单(第一屏、猜你喜欢) -> 退出登录'
        
        self.session.api('/api/mg/auth/user/login')
        menu_id = self.menus.random()
        ret = self.action_Channel(menu_id)
        self.assertTrue(ret)


        