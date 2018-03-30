#!/usr/bin/env Python
# -*- coding:utf-8 -*-


'''test_case_08_login_channelGuess_goodsDetail_loginout.py  登录 -> 二级菜单页(第一屏/猜你喜欢) -> [随机选择猜你喜欢列表商品id] -> 商品详情页 -> 退出登录【卖家/买家/游客】'''


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
class channelGuess_goodsDetail(unittest.TestCase):

    '''获取test_user.csv文件'''
    users = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_user.csv')
    '''获取test_menu.csv文件'''
    menus = ReaderCsv('/Users/dabenchen/Documents/davdian_python/test_api_dvd/test_data/test_menu.csv')


    # =====执行测试=====
    def setUp(self):
        print u'-----测试开始-----'

        # 调用DavdianSession()
        self.session = DavdianSession()

    def tearDown(self):
        print u'-----测试结束-----'
        self.session.api('/api/mg/auth/user/logout')

    
    # ==============测试case===================
    '''以下是: 登录 -> 二级菜单页(第一屏/猜你喜欢) -> [随机选择猜你喜欢列表商品id] -> 商品详情页 -> 退出登录'''
    def action_channelGuess_goodsDetail(self, menu_id=None):

        # 请求二级菜单页第一屏
        print u'二级菜单页第一屏'
        # 业务上传参数:menuId
        print "DEBUG\t[%s][%s]" % (u'menu_id', menu_id)
        param = {'menuId': menu_id['menuId']}
        data = self.session.api('/api/mg/sale/channel/getPageFirst', param)
        # self.assertEqual(int(data['code']), 0, data['data'])


        # 请求二级菜单页猜你喜欢
        print u'二级菜单页猜你喜欢'
        print menu_id
        param = {'menuId': menu_id['menuId'], 'pageIndex': menu_id['pageIndex']}
        data = self.session.api('/api/mg/sale/channel/getGuessBody', param)

        '''抽取猜你喜欢列表商品'''
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
                if re.match('^/\d+.html', data['command']['content']):
                    contents.append(data['command']['content'])
        print "DEBUG\t[%s][%s]" % (u'contents', contents)
        print contents

        length = len(contents)
        # print length
        print "DEBUG\t[%s][%s]" % (u'length', length)

        randIndex = random.randint(0, length - 1)
        content = contents[randIndex]

        goodsIdurl = contents[randIndex]
        goodsId = re.findall(r"\d+\d*", goodsIdurl)[0]
        print "DEBUG\t[%s][%s]" % (u'goodsId', goodsId)
        # self.assertEqual(int(data['code']), 0, data['data'])

        
        # 请求商品详情页
        print u'商品详情页'
        param = {'goodsId': goodsId}
        data = self.session.api('/api/mg/good/info/detail', param)
        # print json.dumps(data)
        return True


    # =============执行case===============
    def test_01_seller_channelGuess_goodsDetail(self):
        print u'卖家身份:登录 -> 二级菜单页(第一屏/猜你喜欢) -> [随机选择猜你喜欢商品id] -> 商品详情页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        menu_id = self.menus.random()
        ret = self.action_channelGuess_goodsDetail(menu_id)
        # print ret
        self.assertTrue(ret)


    def test_02_user_channelGuess_goodsDetail(self):
        print u'买家身份:登录 -> 二级菜单页(第一屏/猜你喜欢) -> [随机选择猜你喜欢商品id] -> 商品详情页 -> 退出登录'
        user = self.users.next()
        self.session.api('/api/mg/auth/user/login', user)
        menu_id = self.menus.random()
        ret = self.action_channelGuess_goodsDetail(menu_id)
        self.assertTrue(ret)


    def test_03_no_channelGuess_goodsDetail(self):
        print u'游客身份:登录 -> 二级菜单页(第一屏/猜你喜欢) -> [随机选择猜你喜欢商品id] -> 商品详情页 -> 退出登录'
        menu_id = self.menus.random()
        ret = self.action_channelGuess_goodsDetail(menu_id)
        self.assertTrue(ret)